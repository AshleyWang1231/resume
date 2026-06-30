from __future__ import annotations

import asyncio
import json
import threading
import urllib.error
import urllib.request
from collections.abc import AsyncIterator, Iterator
from typing import Any


async def stream_openai_chat_completion(
    url: str,
    payload: dict[str, Any],
    headers: dict[str, str],
    *,
    timeout: int = 60,
) -> AsyncIterator[dict[str, Any]]:
    body = json.dumps({**payload, "stream": True}).encode("utf-8")
    loop = asyncio.get_running_loop()
    queue: asyncio.Queue[dict[str, Any] | None | Exception] = asyncio.Queue()

    def _worker() -> None:
        try:
            request = urllib.request.Request(url, data=body, headers=headers, method="POST")
            with urllib.request.urlopen(request, timeout=timeout) as response:
                for raw_line in response:
                    line = raw_line.decode("utf-8").strip()
                    if not line.startswith("data: "):
                        continue
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    parsed = json.loads(data)
                    loop.call_soon_threadsafe(queue.put_nowait, parsed)
        except Exception as exc:
            loop.call_soon_threadsafe(queue.put_nowait, exc)
        else:
            loop.call_soon_threadsafe(queue.put_nowait, None)

    threading.Thread(target=_worker, daemon=True).start()

    while True:
        item = await queue.get()
        if isinstance(item, Exception):
            raise item
        if item is None:
            break
        yield item


def iter_openai_chat_completion_sync(
    url: str,
    payload: dict[str, Any],
    headers: dict[str, str],
    *,
    timeout: int = 60,
) -> Iterator[dict[str, Any]]:
    body = json.dumps({**payload, "stream": True}).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            for raw_line in response:
                line = raw_line.decode("utf-8").strip()
                if not line.startswith("data: "):
                    continue
                data = line[6:]
                if data == "[DONE]":
                    break
                yield json.loads(data)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"stream request failed: {exc.code} {detail[:240]}") from exc
