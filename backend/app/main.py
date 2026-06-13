from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.resume_data import RESUME_FACTS, SUGGESTED_QUESTIONS


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500)
    language: str = Field(default="en", pattern="^(en|zh)$")


class EvidenceCard(BaseModel):
    title: str
    company: str
    summary: str
    evidence: list[str]
    skills: list[str]


class ChatResponse(BaseModel):
    answer: str
    evidence: list[EvidenceCard]
    suggested_questions: list[str]


app = FastAPI(title="Lu Wang Resume Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=False,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    matches = _find_matches(request.message)
    if not matches:
        matches = RESUME_FACTS[:2]

    evidence = [
        EvidenceCard(
            title=item["title"],
            company=item["company"],
            summary=item["summary_zh" if request.language == "zh" else "summary_en"],
            evidence=item["evidence"],
            skills=item["skills"],
        )
        for item in matches[:3]
    ]

    return ChatResponse(
        answer=_build_answer(request.language, evidence),
        evidence=evidence,
        suggested_questions=SUGGESTED_QUESTIONS[request.language],
    )


def _find_matches(message: str) -> list[dict[str, object]]:
    query = message.lower()
    scored: list[tuple[int, dict[str, object]]] = []
    for item in RESUME_FACTS:
        score = sum(1 for keyword in item["keywords"] if keyword in query)
        if score:
            scored.append((score, item))
    return [item for _, item in sorted(scored, key=lambda pair: pair[0], reverse=True)]


def _build_answer(language: str, evidence: list[EvidenceCard]) -> str:
    if language == "zh":
        project_names = "、".join(card.title for card in evidence)
        return f"根据简历，汪露的相关经验主要体现在：{project_names}。这些项目覆盖 Agent、Tool Calling、Streaming、个性化、结构化输出和 Text2SQL 等方向，并且包含可量化结果。"

    project_names = ", ".join(card.title for card in evidence)
    return f"Based on the resume, Lu's relevant experience is strongest in: {project_names}. These projects cover Agent workflows, Tool Calling, Streaming, personalization, structured output, and Text2SQL, with measurable delivery outcomes."
