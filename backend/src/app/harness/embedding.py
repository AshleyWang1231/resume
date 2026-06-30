from __future__ import annotations

import json
import os
import urllib.request
from typing import Any


def embed(texts: list[str]) -> list[list[float]]:
    api_key = os.getenv("QWEN_API_KEY") or os.getenv("DASHSCOPE_API_KEY") or os.getenv("EMBEDDING_API_KEY")
    base_url = (os.getenv("QWEN_BASE_URL") or "https://dashscope.aliyuncs.com/compatible-mode/v1").rstrip("/")
    model = os.getenv("EMBEDDING_MODEL") or "text-embedding-v3"

    if not api_key:
        raise RuntimeError("No embedding API key configured (QWEN_API_KEY / DASHSCOPE_API_KEY / EMBEDDING_API_KEY)")

    body = json.dumps({"model": model, "input": texts}).encode()
    req = urllib.request.Request(
        f"{base_url}/embeddings",
        data=body,
        headers={"authorization": f"Bearer {api_key}", "content-type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data: dict[str, Any] = json.loads(resp.read().decode())

    items = sorted(data["data"], key=lambda x: x["index"])
    return [item["embedding"] for item in items]
