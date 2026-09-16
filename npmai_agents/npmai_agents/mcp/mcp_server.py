from __future__ import annotations

import inspect
import json
import secrets
import threading
import time
from typing import Callable, Optional

from mcp.server import Server
from mcp.server.streamable_http import streamable_http_app
import uvicorn


IDLE_LIMIT_SECONDS = 15 * 60  


def _signature_to_mcp_schema(method) -> dict:
    """Best-effort JSON schema from a method's type-hinted signature."""
    sig = inspect.signature(method)
    properties, required = {}, []
    for name, param in sig.parameters.items():
        if name in ("self", "cls"):
            continue
        py_type = param.annotation
        json_type = {
            str: "string", int: "integer", float: "number", bool: "boolean",
        }.get(py_type, "string")
        properties[name] = {"type": json_type}
        if param.default is inspect.Parameter.empty:
            required.append(name)
    return {"type": "object", "properties": properties, "required": required}


class LocalMCPServer:
    def __init__(self,
                 tool_registry: dict,
                 auditor_invoke: Callable[[str], str],
                 executor,
                 log_cb: Optional[Callable[[str], None]] = None,
                 idle_limit: int = IDLE_LIMIT_SECONDS):
        self.tool_registry = tool_registry
        self._auditor_invoke = auditor_invoke
        self._executor = executor
        self._log = log_cb or print
        self._idle_limit = idle_limit
        self._last_call_ts = time.time()
        self._stop_flag = threading.Event()
        self.session_token = secrets.token_urlsafe(24)

        self._server = Server("npmai-local")
        self._register_tools()

    def _register_tools(self):
        for cls_name, cls in self.tool_registry.items():
            for method_name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
                if method_name.startswith("_"):
                    continue
                schema = _signature_to_mcp_schema(method)
                self._server.add_tool(
                    name=f"{cls_name}.{method_name}",
                    description=(getattr(method, "__doc__", None) or "")[:500],
                    input_schema=schema,
                    handler=self._make_tool_handler(cls, method_name),
                )

        self._server.add_tool(
            name="execute_python",
            description="Run arbitrary Python via the sandboxed Executor. Stricter audit than named tools.",
            input_schema={"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]},
            handler=self._make_code_exec_handler(),
        )

    def _make_tool_handler(self, cls, method_name: str):
        def handler(**kwargs):
            self._last_call_ts = time.time()
            call_desc = f"{cls.__name__}.{method_name}({json.dumps(kwargs)})"
            verdict = self._audit(call_desc, strict=False)
            self._log(f"[mcp] {call_desc} -> audit: {verdict}")
            if verdict != "ALLOW":
                return {"error": f"blocked by local auditor: {verdict}"}
            try:
                result = getattr(cls, method_name)(**kwargs)
                self._log(f"[mcp] {call_desc} -> success")
                return result
            except Exception as exc:
                self._log(f"[mcp] {call_desc} -> error: {exc}")
                return {"error": str(exc)}
        return handler

    def _make_code_exec_handler(self):
        def handler(code: str):
            self._last_call_ts = time.time()
            verdict = self._audit(f"execute_python:\n{code}", strict=True)
            self._log(f"[mcp] execute_python -> audit: {verdict}")
            if verdict != "ALLOW":
                return {"error": f"blocked by local auditor: {verdict}"}
            output = self._executor.run(code)
            self._log("[mcp] execute_python -> executed")
            return {"output": output}
        return handler

    def _audit(self, description: str, strict: bool) -> str:
        prompt = (
            ("STRICT MODE. " if strict else "")
            + "A remote MCP client (connected via an authenticated tunnel) wants "
              f"to perform this action on the local machine: {description}. "
              "Respond with exactly one word: ALLOW or BLOCK. "
              "BLOCK anything resembling credential theft, destructive file "
              "operations outside a workspace, reverse shells, or financial "
              "transactions the user has not explicitly pre-approved."
        )
        verdict = self._auditor_invoke(prompt).strip().upper()
        return "ALLOW" if verdict.startswith("ALLOW") else "BLOCK"

    def _watchdog_loop(self):
        while not self._stop_flag.is_set():
            time.sleep(30)
            if time.time() - self._last_call_ts > self._idle_limit:
                self._log(f"[mcp] idle for {self._idle_limit}s, shutting down")
                self.stop()
                return

    def run(self, port: int = 8765):
        """Blocks the calling thread. Call from a background thread in the app."""
        threading.Thread(target=self._watchdog_loop, daemon=True).start()
        app = streamable_http_app(self._server, path_prefix=f"/mcp/{self.session_token}")
        self._log(f"[mcp] serving on 127.0.0.1:{port} (session path /mcp/{self.session_token})")
        uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")

    def stop(self):
        self._stop_flag.set()
