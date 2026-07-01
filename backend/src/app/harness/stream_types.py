# Layer 3 — Execution Orchestration (event types)
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class StreamEvent:
    event: str
    data: Any
