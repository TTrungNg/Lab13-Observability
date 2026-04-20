from __future__ import annotations

import time
import uuid

from starlette.datastructures import Headers, MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from structlog.contextvars import bind_contextvars, clear_contextvars


class CorrelationIdMiddleware:
    """Pure ASGI middleware (avoids BaseHTTPMiddleware contextvar bugs with OpenTelemetry/Langfuse)."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        clear_contextvars()

        headers = Headers(scope=scope)
        incoming = headers.get("x-request-id")
        if incoming and incoming.strip():
            correlation_id = incoming.strip()
        else:
            correlation_id = f"req-{uuid.uuid4().hex[:8]}"

        bind_contextvars(correlation_id=correlation_id)

        scope.setdefault("state", {})
        scope["state"]["correlation_id"] = correlation_id

        start = time.perf_counter()

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                response_headers = MutableHeaders(scope=message)
                response_headers["x-request-id"] = correlation_id
                elapsed_ms = int((time.perf_counter() - start) * 1000)
                response_headers["x-response-time-ms"] = str(elapsed_ms)
            await send(message)

        await self.app(scope, receive, send_wrapper)
