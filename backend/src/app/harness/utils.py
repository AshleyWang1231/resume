"""Shared small utilities used across harness modules.

Extracted here to eliminate copy-paste between clients.
"""
from __future__ import annotations

import json
import re
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


# ── Output sanitisation ───────────────────────────────────────────────────────

# Strip XML/HTML tags the model sometimes wraps output in (e.g. <error>, <answer>)
_TAG_RE = re.compile(r"</?[a-z][a-z0-9]*(?:\s[^>]*)?>", re.IGNORECASE)

# Strip markdown: headers (### / ## / #), bold/italic (**x** / *x* / __x__ / _x_)
_HEADER_RE = re.compile(r"^#{1,6}\s+", re.MULTILINE)
_BOLD_ITALIC_RE = re.compile(r"(\*{1,3}|_{1,3})(.+?)\1")

# Strip leading list markers (- item / * item / 1. item) that the model emits
_LIST_RE = re.compile(r"^[\-\*]\s+|^\d+\.\s+", re.MULTILINE)


def sanitise_answer(text: str) -> str:
    """Remove XML tags, markdown headers, and bold/italic from model output.

    Applied as a last-resort post-processing step after the LLM returns its
    answer, in case the model ignores the formatting instructions in the system
    prompt.
    """
    text = _TAG_RE.sub("", text)          # <error>…</error> → stripped
    text = _HEADER_RE.sub("", text)       # ### Heading → ""
    text = _BOLD_ITALIC_RE.sub(r"\2", text)  # **text** → text
    text = _LIST_RE.sub("", text)         # - item → item
    # Collapse lines that became blank after stripping
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
