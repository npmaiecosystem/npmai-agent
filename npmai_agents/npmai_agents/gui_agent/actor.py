from __future__ import annotations

import time
from typing import Callable, Optional

from .perception import Element, ScreenState


class ActionExecutor:
    """
    Thin wrapper around mss (screenshots) + pyautogui (input).
    Both are optional deps, installed lazily via the same ensure() pattern
    used elsewhere in npmai_agents -- imported inside __init__ rather than
    at module load time so importing gui_agent doesn't force the install.
    """

    def __init__(self, log_cb: Optional[Callable[[str], None]] = None,
                 action_delay: float = 0.15):
        import mss
        import pyautogui

        self._mss = mss.mss()
        self._pg = pyautogui
        self._pg.FAILSAFE = True 
        self._log = log_cb or (lambda msg: None)
        self._action_delay = action_delay  

    def screenshot(self, monitor_index: int = 0, out_path: Optional[str] = None) -> ScreenState:
        monitor = self._mss.monitors[monitor_index + 1]  
        shot = self._mss.grab(monitor)
        path = out_path or f"/tmp/npmai_gui_{int(time.time() * 1000)}.png"
        import mss.tools
        mss.tools.to_png(shot.rgb, shot.size, output=path)

        dpi_scale = self._detect_dpi_scale()
        self._log(f"[gui] screenshot captured -> {path}")
        return ScreenState(screenshot_path=path, monitor_index=monitor_index, dpi_scale=dpi_scale)

    def _detect_dpi_scale(self) -> float:
        try:
            import ctypes
            return ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100.0
        except Exception:
            return 1.0  

    def click(self, element: Element, button: str = "left"):
        x, y = element.center
        self._log(f"[gui] click({element.name!r} @ {x},{y})")
        self._pg.click(x, y, button=button)
        time.sleep(self._action_delay)

    def double_click(self, element: Element):
        x, y = element.center
        self._log(f"[gui] double_click({element.name!r} @ {x},{y})")
        self._pg.doubleClick(x, y)
        time.sleep(self._action_delay)

    def type_text(self, element: Element, text: str, clear_first: bool = True):
        x, y = element.center
        self._log(f"[gui] type_into({element.name!r}): {text[:40]!r}{'...' if len(text) > 40 else ''}")
        self._pg.click(x, y)
        time.sleep(0.05)
        if clear_first:
            self._pg.hotkey("ctrl", "a")
            self._pg.press("delete")
        self._pg.typewrite(text, interval=0.02)
        time.sleep(self._action_delay)

    def scroll(self, direction: str, amount: int = 3):
        self._log(f"[gui] scroll({direction}, {amount})")
        clicks = amount if direction == "up" else -amount
        self._pg.scroll(clicks)
        time.sleep(self._action_delay)

    def key_combo(self, keys: list[str]):
        self._log(f"[gui] key_combo({'+'.join(keys)})")
        self._pg.hotkey(*keys)
        time.sleep(self._action_delay)

    def press_key(self, key: str):
        self._log(f"[gui] press_key({key})")
        self._pg.press(key)
        time.sleep(self._action_delay)
