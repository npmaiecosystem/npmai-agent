from __future__ import annotations

import re
import subprocess
import threading
import time
from typing import Callable, Optional


class CloudflareTunnel:
    URL_PATTERN = re.compile(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")

    def __init__(self, local_port: int, log_cb: Optional[Callable[[str], None]] = None):
        self.local_port = local_port
        self._log = log_cb or print
        self._proc: Optional[subprocess.Popen] = None
        self._reader_thread: Optional[threading.Thread] = None
        self.url: Optional[str] = None

    def start(self, timeout: float = 15.0) -> str:
        if self._proc is not None:
            raise RuntimeError("tunnel already running; call stop() first")

        try:
            self._proc = subprocess.Popen(
                ["cloudflared", "tunnel", "--url", f"http://127.0.0.1:{self.local_port}"],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
            )
        except FileNotFoundError as exc:
            raise RuntimeError(
                "cloudflared binary not found on PATH. Install it from "
                "https://github.com/cloudflare/cloudflared/releases and retry."
            ) from exc

        found_url: list[str] = []
        done = threading.Event()

        def _read_output():
            for line in self._proc.stdout:  
                line = line.strip()
                if line:
                    self._log(f"[cloudflared] {line}")
                match = self.URL_PATTERN.search(line)
                if match and not found_url:
                    found_url.append(match.group(0))
                    done.set()

        self._reader_thread = threading.Thread(target=_read_output, daemon=True)
        self._reader_thread.start()

        if not done.wait(timeout=timeout):
            self.stop()
            raise TimeoutError("cloudflared did not report a public URL in time")

        self.url = found_url[0]
        self._log(f"[cloudflared] tunnel live: {self.url}")
        return self.url

    def is_alive(self) -> bool:
        return self._proc is not None and self._proc.poll() is None

    def stop(self):
        if self._proc is not None:
            self._proc.terminate()
            try:
                self._proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._proc.kill()
            self._proc = None
        self.url = None
        self._log("[cloudflared] tunnel stopped")
