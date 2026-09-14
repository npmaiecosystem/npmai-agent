from __future__ import annotations

import time
from typing import Optional

from .perception import Element


class ElementCache:
    def __init__(self, ttl_seconds: float = 45.0):
        self._store: dict[str, tuple[Element, float]] = {}
        self._ttl = ttl_seconds

    @staticmethod
    def _key(description: str, window_title: Optional[str]) -> str:
        return f"{(window_title or '').lower()}::{description.lower().strip()}"

    def get(self, description: str, window_title: Optional[str] = None) -> Optional[Element]:
        entry = self._store.get(self._key(description, window_title))
        if not entry:
            return None
        element, _ = entry
        return element

    def still_valid(self, element: Element) -> bool:
        key = self._key(element.name, element.window_title)
        entry = self._store.get(key)
        if not entry:
            return False
        _, cached_at = entry
        return (time.time() - cached_at) < self._ttl

    def put(self, description: str, element: Element):
        cached = Element(
            name=element.name, role=element.role, bbox=element.bbox,
            confidence=element.confidence, source="cache",
            window_title=element.window_title, process_name=element.process_name,
        )
        self._store[self._key(description, element.window_title)] = (cached, time.time())

    def invalidate(self, description: str, window_title: Optional[str] = None):
        self._store.pop(self._key(description, window_title), None)

    def clear(self):
        self._store.clear()
