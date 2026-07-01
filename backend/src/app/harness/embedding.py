from __future__ import annotations

import json
import os
from typing import Any

import httpx


def _do_embed(texts: list[str]) -> list[list[float]]:
    """Shared implementation called by both sync and async wrappers."""
    api_key = os.getenv("QWEN_API_KEY") or os.getenv("DASHSCOPE_API_KEY") or os.getenv("EMBEDDING_API_KEY")
    base_url = (os.getenv("QWEN_BASE_URL") or "https://dashscope.aliyuncs.com/compatible-mode/v1").rstrip("/")
    model = os.getenv("EMBEDDING_MODEL") or "text-embedding-v3"

    if not api_key:
        raise RuntimeError("No embedding API key configured (QWEN_API_KEY / DASHSCOPE_API_KEY / EMBEDDING_API_KEY)")

    with httpx.Client(timeout=30) as client:
        try:
            resp = client.post(
                f"{base_url}/embeddings",
                headers={"authorization": f"Bearer {api_key}", "content-type": "application/json"},
                content=json.dumps({"model": model, "input": texts}).encode(),
            )
            resp.raise_for_status()
            data: dict[str, Any] = resp.json()
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(f"Embedding request failed: {exc.response.status_code} {exc.response.text[:240]}") from exc

    items = sorted(data["data"], key=lambda x: x["index"])
    return [item["embedding"] for item in items]


def embed_sync(texts: list[str]) -> list[list[float]]:
    """Synchronous embedding call — used for FAISS index initialisation at startup."""
    return _do_embed(texts)


async def embed(texts: list[str]) -> list[list[float]]:
    """Async embedding call — used during request handling."""
    return _do_embed(texts)
