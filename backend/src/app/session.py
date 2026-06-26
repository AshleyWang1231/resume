from __future__ import annotations

import time
from collections import OrderedDict
from typing import Any


class SessionStore:
    """In-process session store for multi-turn conversation history.

    Intentionally simple — bounded LRU with TTL expiry. Senior engineers
    know when NOT to reach for Redis: a stateless FC function with modest
    concurrency doesn't need an external store for demo conversations.
    """

    _MAX_SESSIONS = 500
    _TTL_SECONDS = 60 * 30  # 30 min

    def __init__(self) -> None:
        self._store: OrderedDict[str, dict[str, Any]] = OrderedDict()

    def get_history(self, session_id: str) -> list[dict[str, str]]:
        entry = self._store.get(session_id)
        if not entry:
            return []
        if time.time() - entry["ts"] > self._TTL_SECONDS:
            del self._store[session_id]
            return []
        return list(entry["history"])

    def append(self, session_id: str, role: str, content: str) -> None:
        self._evict_expired()
        if session_id not in self._store:
            if len(self._store) >= self._MAX_SESSIONS:
                self._store.popitem(last=False)
            self._store[session_id] = {"ts": time.time(), "history": []}
        self._store[session_id]["history"].append({"role": role, "content": content})
        self._store[session_id]["ts"] = time.time()
        self._store.move_to_end(session_id)

    def _evict_expired(self) -> None:
        now = time.time()
        expired = [k for k, v in self._store.items() if now - v["ts"] > self._TTL_SECONDS]
        for k in expired:
            del self._store[k]


session_store = SessionStore()
