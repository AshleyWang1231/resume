"""Shared small utilities used across harness modules.

Extracted here to eliminate copy-paste between clients.
"""
from __future__ import annotations

import json
from typing import Any

from app.models import EvidenceCard


def dedupe_evidence(items: list[EvidenceCard]) -> list[EvidenceCard]:
    """Return items with duplicates removed, preserving first-seen order."""
    seen: set[str] = set()
    deduped: list[EvidenceCard] = []
    for item in items:
        key = item.id or item.title
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def parse_arguments(raw_arguments: Any) -> dict[str, Any]:
    """Safely parse tool-call arguments from a raw JSON string or dict."""
    if isinstance(raw_arguments, dict):
        return raw_arguments
    if not raw_arguments:
        return {}
    try:
        parsed = json.loads(str(raw_arguments))
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def log(event: str, **kwargs: Any) -> None:
    """Emit a structured JSON log line to stdout."""
    print(json.dumps({"event": event, **kwargs}, ensure_ascii=False))
