from __future__ import annotations

import threading
from typing import Callable, Optional

from .mcp_server import LocalMCPServer
from .tunnel import CloudflareTunnel


class MCPBridge:
    def __init__(self,
                 tool_registry: dict,
                 auditor_invoke: Callable[[str], str],
                 executor,
                 local_port: int = 8765,
                 log_cb: Optional[Callable[[str], None]] = None):
        self._log = log_cb or print
        self.local_port = local_port
        self._server = LocalMCPServer(
            tool_registry=tool_registry,
            auditor_invoke=auditor_invoke,
            executor=executor,
            log_cb=self._log,
        )
        self._tunnel = CloudflareTunnel(local_port=local_port, log_cb=self._log)
        self._server_thread: Optional[threading.Thread] = None
        self.full_url: Optional[str] = None

    def start(self) -> str:
        self._server_thread = threading.Thread(
            target=self._server.run, kwargs={"port": self.local_port}, daemon=True
        )
        self._server_thread.start()

        base_url = self._tunnel.start()
        self.full_url = f"{base_url}/mcp/{self._server.session_token}"
        self._log(f"[bridge] ready: {self.full_url}")
        return self.full_url

    def stop(self):
        self._server.stop()
        self._tunnel.stop()
        self.full_url = None
        self._log("[bridge] stopped -- URL is now dead")

    def is_alive(self) -> bool:
        return self._tunnel.is_alive() and (self._server_thread is not None and self._server_thread.is_alive())
