from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


Language = Literal["en", "zh"]


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500)
    language: Language = "en"
    session_id: str | None = None


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
    session_id: str | None = None
    source: Literal["openai", "qwen", "deepseek", "workers_ai", "fallback"] = "fallback"
    tools_called: list[str] = Field(default_factory=list)


class AgentContext(BaseModel):
    request_id: str
    message: str
    language: Language
    intent: str
    session_id: str


class ProjectCard(BaseModel):
    id: str
    title: str
    company: str
    period: str
    summary_en: str
    summary_zh: str
    impact: list[str]
    skills: list[str]
    highlight: bool = False


class ArchitectureNode(BaseModel):
    id: str
    label: str
    type: Literal["frontend", "backend", "llm", "data", "infra"]
    description: str


class ArchitectureEdge(BaseModel):
    from_id: str
    to_id: str
    label: str


class ArchitectureResponse(BaseModel):
    nodes: list[ArchitectureNode]
    edges: list[ArchitectureEdge]
    summary_en: str
    summary_zh: str
