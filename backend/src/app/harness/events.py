# Layer 3 — Execution Orchestration (SSE serialisation)
from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Any

from app.models import ChatResponse


def sse_event(event: str, data: Any) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


async def stream_chat_response(response: ChatResponse) -> AsyncIterator[str]:
    yield sse_event(
        "metadata",
        {
            "request_id": response.request_id,
            "source": response.source,
            "tools_called": response.tools_called,
        },
    )

    for tool_name in response.tools_called:
        yield sse_event("tool_call", {"name": tool_name})
    if response.tools_called:
        yield sse_event("tool_result", {"count": len(response.evidence)})

    for chunk in _chunk_text(response.answer):
        yield sse_event("answer_delta", {"text": chunk})

    yield sse_event("evidence", [item.model_dump() for item in response.evidence])
    yield sse_event("done", {
        "request_id": response.request_id,
        "session_id": response.session_id,
        "suggested_questions": response.suggested_questions,
    })


def _chunk_text(text: str, chunk_size: int = 28) -> list[str]:
    if len(text) <= chunk_size:
        return [text]
    chunks: list[str] = []
    current = ""
    for token in text.split(" "):
        next_value = f"{current} {token}".strip()
        if len(next_value) > chunk_size and current:
            chunks.append(current + " ")
            current = token
        else:
            current = next_value
    if current:
        chunks.append(current)
    return chunks

