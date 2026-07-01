# Layer 5 — Evaluation & Observability
from __future__ import annotations

import json
import time
from collections.abc import Callable
from typing import Any


def now_ms() -> float:
    return time.perf_counter() * 1000


def log_request(fields: dict[str, Any]) -> None:
    print(json.dumps(fields, ensure_ascii=False, sort_keys=True))


async def with_request_logging(
    route: str,
    handler: Callable[[], Any],
    base_fields: dict[str, Any],
) -> Any:
    start = now_ms()
    try:
        result = await handler()
    except Exception as exc:
        log_request(
            {
                **base_fields,
                "route": route,
                "status": "error",
                "error_type": exc.__class__.__name__,
                "error_message": str(exc),
                "latency_ms": round(now_ms() - start),
            }
        )
        raise

    log_request(
        {
            **base_fields,
            "request_id": getattr(result, "request_id", None),
            "route": route,
            "status": "success",
            "source": getattr(result, "source", None),
            "tools_called": getattr(result, "tools_called", []),
            "evidence_count": len(getattr(result, "evidence", [])),
            "latency_ms": round(now_ms() - start),
        }
    )
    return result
