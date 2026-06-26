from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


Language = Literal["en", "zh"]


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500)
    language: Language = "en"


class EvidenceCard(BaseModel):
    id: str | None = None
    title: str
    company: str
    summary: str
    evidence: list[str]
    skills: list[str]


class ChatResponse(BaseModel):
    answer: str
    evidence: list[EvidenceCard]
    suggested_questions: list[str]
    request_id: str | None = None
    source: Literal["openai", "qwen", "deepseek", "fallback"] = "fallback"
    tools_called: list[str] = Field(default_factory=list)


class AgentContext(BaseModel):
    request_id: str
    message: str
    language: Language
    intent: str
