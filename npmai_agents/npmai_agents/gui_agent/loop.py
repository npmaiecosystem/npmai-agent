from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, Optional

from .actor import ActionExecutor
from .cache import ElementCache
from .perception import AccessibilityReader, Element, VisualGrounder


@dataclass
class GUIStepResult:
    success: bool
    element_used: Optional[Element] = None
    note: str = ""
    screenshot_before: Optional[str] = None
    screenshot_after: Optional[str] = None


class GUIAgentLoop:
    """
    intent schema (what AgentBrain's planner emits for mode="gui" steps):
        {
            "action": "click" | "type" | "scroll" | "wait" | "key_combo",
            "target": "<natural language description of the element>",
            "value": "<text to type, or None>",
            "window_hint": "<expected window title, optional>",
        }
    """

    def __init__(self,
                 actor: ActionExecutor,
                 grounder: VisualGrounder,
                 auditor_invoke: Callable[[str], str],
                 verifier_invoke: Callable[[str], str],
                 log_cb: Optional[Callable[[str], None]] = None,
                 max_retries: int = 3):
        self.actor = actor
        self.a11y = AccessibilityReader()
        self.grounder = grounder
        self._auditor_invoke = auditor_invoke  
        self._verifier_invoke = verifier_invoke  
        self._cache = ElementCache()
        self._log = log_cb or (lambda msg: None)
        self.max_retries = max_retries


    def resolve_element(self, description: str, screen_w: int, screen_h: int) -> Optional[Element]:
        el = self.a11y.find(description)
        if el:
            self._log(f"[gui] resolved '{description}' via a11y")
            return el

        cached = self._cache.get(description)
        if cached and self._cache.still_valid(cached):
            self._log(f"[gui] resolved '{description}' via cache")
            return cached

        shot = self.actor.screenshot()
        el = self.grounder.locate(shot.screenshot_path, description, screen_w, screen_h)
        if el:
            self._log(f"[gui] resolved '{description}' via vision (confidence {el.confidence})")
            self._cache.put(description, el)
        return el

    def execute_step(self, intent: dict, screen_w: int = 1920, screen_h: int = 1080,
                      _attempt: int = 0) -> GUIStepResult:
        verdict = self._audit_intent(intent)
        if verdict != "ALLOW":
            self._log(f"[gui] BLOCKED by auditor: {intent} -> {verdict}")
            return GUIStepResult(success=False, note=f"blocked by auditor: {verdict}")

        if intent["action"] == "wait":
            return self._wait_for(intent)

        element = self.resolve_element(intent["target"], screen_w, screen_h)
        if not element:
            return GUIStepResult(success=False, note=f"element not found: {intent['target']!r}")

        before = self.actor.screenshot()
        
        self._act(intent, element)

        after = self.actor.screenshot()
        changed = self._screens_differ(before.screenshot_path, after.screenshot_path)
        ok = changed or self._verify_via_llm(intent, after.screenshot_path)

        if not ok and _attempt < self.max_retries:
            self._log(f"[gui] step did not verify, retrying (attempt {_attempt + 1}/{self.max_retries})")
            self._cache.invalidate(intent["target"])  
            return self.execute_step(intent, screen_w, screen_h, _attempt=_attempt + 1)

        return GUIStepResult(
            success=ok, element_used=element,
            note="" if ok else "verification failed after retries",
            screenshot_before=before.screenshot_path,
            screenshot_after=after.screenshot_path,
        )

    def _act(self, intent: dict, element: Element):
        action = intent["action"]
        if action == "click":
            self.actor.click(element)
        elif action == "type":
            self.actor.type_text(element, intent.get("value", ""))
        elif action == "scroll":
            self.actor.scroll(intent.get("value", "down"))
        elif action == "key_combo":
            self.actor.key_combo(intent.get("value", []))
        else:
            raise ValueError(f"unknown gui action: {action!r}")

    def _wait_for(self, intent: dict, poll_interval: float = 1.0, timeout: float = 30.0) -> GUIStepResult:
        deadline = time.time() + intent.get("timeout", timeout)
        while time.time() < deadline:
            el = self.a11y.find(intent["target"])
            if el:
                return GUIStepResult(success=True, element_used=el)
            time.sleep(poll_interval)
        return GUIStepResult(success=False, note=f"timed out waiting for {intent['target']!r}")

    def _audit_intent(self, intent: dict) -> str:
        """
        Sends the INTENT, not code, to the auditor role. This is the
        GUI-specific twin of AgentBrain's code auditor: it reviews what's
        about to be clicked/typed rather than reviewing generated source.
        """
        prompt = (
            "A GUI automation agent is about to perform this action on the "
            f"user's real screen: {intent}. "
            "Respond with exactly one word: ALLOW or BLOCK. "
            "BLOCK if this looks like it could submit a payment, delete data, "
            "send a message, or perform an irreversible action the user did "
            "not clearly ask for in the current task."
        )
        verdict = self._auditor_invoke(prompt).strip().upper()
        return "ALLOW" if verdict.startswith("ALLOW") else "BLOCK"

    def _verify_via_llm(self, intent: dict, screenshot_after: str) -> bool:
        prompt = (
            f"After performing this GUI action: {intent}, here is a screenshot "
            "of the resulting screen state. Did the action appear to succeed? "
            "Respond with exactly one word: YES or NO."
        )
        try:
            answer = self._verifier_invoke(prompt).strip().upper()
        except NotImplementedError:
            return True  
        return answer.startswith("YES")

    @staticmethod
    def _screens_differ(before_path: str, after_path: str, threshold: float = 0.02) -> bool:
        """Cheap pixel-diff so most steps don't need an LLM verify call at all."""
        from PIL import Image, ImageChops
        import numpy as np

        a = Image.open(before_path).convert("RGB")
        b = Image.open(after_path).convert("RGB")
        if a.size != b.size:
            return True
        diff = ImageChops.difference(a, b)
        arr = np.asarray(diff)
        changed_fraction = (arr > 25).mean()
        return changed_fraction > threshold
