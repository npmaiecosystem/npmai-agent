from __future__ import annotations

import json
import platform
import re
import time
from dataclasses import dataclass, field
from typing import Literal, Optional


@dataclass
class Element:
    """A single actionable UI element, regardless of which layer found it."""
    name: str
    role: str 
    bbox: tuple[int, int, int, int] 
    confidence: float
    source: Literal["a11y", "cache", "vision"]
    window_title: Optional[str] = None
    process_name: Optional[str] = None

    @property
    def center(self) -> tuple[int, int]:
        x, y, w, h = self.bbox
        return (x + w // 2, y + h // 2)


@dataclass
class ScreenState:
    """A single captured observation of the screen."""
    screenshot_path: str
    monitor_index: int
    dpi_scale: float
    timestamp: float = field(default_factory=time.time)


class AccessibilityReader:
    """
    Layer 1 perception: OS accessibility tree.

    No LLM call, near-zero latency, exact coordinates. Always tried before
    falling back to vision. Platform backend is selected lazily so this
    module imports cleanly even on a machine missing the optional deps --
    matches the existing `ensure()` optional-install pattern in core.py.
    """

    def __init__(self):
        self._system = platform.system()  # "Windows", "Darwin", "Linux"
        self._backend = None  

    def _get_backend(self):
        if self._backend is not None:
            return self._backend

        if self._system == "Windows":
            import uiautomation as auto  
            self._backend = ("windows", auto)
        elif self._system == "Darwin":
            import atomac  
            self._backend = ("macos", atomac)
        else:
            import pyatspi  
            self._backend = ("linux", pyatspi)
        return self._backend

    def get_focused_window_tree(self) -> list[Element]:
        """Walk the accessibility tree of the currently focused window."""
        kind, backend = self._get_backend()
        elements: list[Element] = []

        if kind == "windows":
            win = backend.GetFocusedControl()
            if win is None:
                return elements
            top = win.GetTopLevelControl()
            window_title = top.Name if top else None
            process_name = getattr(top, "ProcessName", None) if top else None

            def walk(ctrl, depth=0, max_depth=12):
                if depth > max_depth:
                    return
                try:
                    rect = ctrl.BoundingRectangle
                    if rect and rect.width() > 0 and rect.height() > 0:
                        elements.append(
                            Element(
                                name=ctrl.Name or "",
                                role=str(ctrl.ControlTypeName or "unknown"),
                                bbox=(rect.left, rect.top, rect.width(), rect.height()),
                                confidence=1.0,
                                source="a11y",
                                window_title=window_title,
                                process_name=process_name,
                            )
                        )
                except Exception:
                    pass
                for child in ctrl.GetChildren():
                    walk(child, depth + 1, max_depth)

            walk(top or win)

        elif kind == "macos":
            app = backend.getFrontmostApp()
            window_title = getattr(app, "AXTitle", None)

            def walk(node, depth=0, max_depth=12):
                if depth > max_depth:
                    return
                try:
                    pos = node.AXPosition
                    size = node.AXSize
                    if pos and size:
                        elements.append(
                            Element(
                                name=getattr(node, "AXTitle", "") or getattr(node, "AXDescription", "") or "",
                                role=getattr(node, "AXRole", "unknown"),
                                bbox=(int(pos[0]), int(pos[1]), int(size[0]), int(size[1])),
                                confidence=1.0,
                                source="a11y",
                                window_title=window_title,
                            )
                        )
                except Exception:
                    pass
                for child in getattr(node, "AXChildren", []) or []:
                    walk(child, depth + 1, max_depth)

            walk(app)

        else:  
            desktop = backend.Registry.getDesktop(0)

            def walk(node, depth=0, max_depth=12):
                if depth > max_depth or node is None:
                    return
                try:
                    component = node.queryComponent()
                    extents = component.getExtents(pyatspi.DESKTOP_COORDS)
                    if extents.width > 0 and extents.height > 0:
                        elements.append(
                            Element(
                                name=node.name or "",
                                role=str(node.getRoleName()),
                                bbox=(extents.x, extents.y, extents.width, extents.height),
                                confidence=1.0,
                                source="a11y",
                            )
                        )
                except Exception:
                    pass
                for i in range(node.childCount):
                    walk(node.getChildAtIndex(i), depth + 1, max_depth)

            for app in desktop:
                walk(app)

        return elements

    def find(self, description_hint: str, min_score: float = 0.55) -> Optional[Element]:
        """
        Fuzzy-match description_hint against the focused window's element
        names/roles. Returns the best match above min_score, or None so the
        caller falls through to cache -> vision.
        """
        try:
            candidates = self.get_focused_window_tree()
        except Exception:
            return None
        if not candidates:
            return None

        best, best_score = None, 0.0
        hint = description_hint.lower().strip()
        for el in candidates:
            score = _fuzzy_score(hint, f"{el.name} {el.role}".lower())
            if score > best_score:
                best, best_score = el, score

        return best if best_score >= min_score else None


def _fuzzy_score(a: str, b: str) -> float:
    """Lightweight token-overlap fuzzy match (no extra dependency required)."""
    a_tokens = set(re.findall(r"\w+", a))
    b_tokens = set(re.findall(r"\w+", b))
    if not a_tokens or not b_tokens:
        return 0.0
    overlap = len(a_tokens & b_tokens)
    return overlap / max(len(a_tokens), 1)


class VisualGrounder:
    """
    Layer 2 perception: vision-model fallback.

    Requires an LLMBackend whose subclass implements invoke_with_image().
    Only called when AccessibilityReader and ElementCache both miss.
    """

    PROMPT_TEMPLATE = (
        "You are looking at a screenshot of a computer screen. "
        "Find the UI element matching this description: \"{description}\".\n"
        "Respond with ONLY a JSON object, no other text, in this exact form:\n"
        '{{"found": true, "x": <int 0-1000>, "y": <int 0-1000>, '
        '"w": <int 0-1000>, "h": <int 0-1000>, "role": "<button|textbox|...>"}}\n'
        "Coordinates are normalized to a 0-1000 scale for both axes "
        "(0,0 = top-left, 1000,1000 = bottom-right). "
        'If no matching element is visible, respond {{"found": false}}.'
    )

    def __init__(self, backend):
        """backend: an LLMBackend instance implementing invoke_with_image()."""
        self.backend = backend

    def locate(self, screenshot_path: str, description: str,
               screen_w: int, screen_h: int) -> Optional[Element]:
        prompt = self.PROMPT_TEMPLATE.format(description=description)
        try:
            raw = self.backend.invoke_with_image(prompt, screenshot_path)
        except NotImplementedError:
            raise RuntimeError(
                f"{type(self.backend).__name__} does not support vision input; "
                "configure a vision-capable backend for the gui_grounder stage."
            )

        data = _extract_json(raw)
        if not data or not data.get("found"):
            return None

       
        x = int(data["x"] / 1000 * screen_w)
        y = int(data["y"] / 1000 * screen_h)
        w = max(1, int(data.get("w", 20) / 1000 * screen_w))
        h = max(1, int(data.get("h", 20) / 1000 * screen_h))

        return Element(
            name=description,
            role=data.get("role", "unknown"),
            bbox=(x, y, w, h),
            confidence=0.75,  
            source="vision",
        )


def _extract_json(text: str) -> Optional[dict]:
    """Vision models sometimes wrap JSON in prose or code fences; salvage it."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None
