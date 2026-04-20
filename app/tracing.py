from __future__ import annotations

import os
from typing import Any

try:
    from langfuse import get_client, observe

    class _LangfuseContext:
        """Shim for the old langfuse_context API (Langfuse v2) on Langfuse v3 SDK."""

        def update_current_trace(self, **kwargs: Any) -> None:
            get_client().update_current_trace(**kwargs)

        def update_current_observation(self, **kwargs: Any) -> None:
            metadata = dict(kwargs.get("metadata") or {})
            usage = kwargs.get("usage_details")
            if usage is not None:
                metadata["usage_details"] = usage
            get_client().update_current_span(metadata=metadata or None)

    langfuse_context = _LangfuseContext()

except Exception:  # pragma: no cover
    def observe(*args: Any, **kwargs: Any):
        def decorator(func):
            return func

        return decorator

    class _DummyContext:
        def update_current_trace(self, **kwargs: Any) -> None:
            return None

        def update_current_observation(self, **kwargs: Any) -> None:
            return None

    langfuse_context = _DummyContext()


def tracing_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))


def flush_langfuse() -> None:
    """Push batched spans to Langfuse immediately (default SDK flush can be several seconds)."""
    if not tracing_enabled():
        return
    try:
        from langfuse import get_client as _get_client

        _get_client().flush()
    except Exception:
        pass
