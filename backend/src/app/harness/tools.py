from __future__ import annotations

import re
from typing import Any

from rank_bm25 import BM25Okapi

from app.models import EvidenceCard, Language
from app.resume_data import RESUME_FACTS


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+|[一-鿿]", text.lower())


def _build_corpus() -> list[list[str]]:
    return [
        _tokenize(
            " ".join([
                item["id"],
                item["title"],
                item["summary_en"],
                item["summary_zh"],
                " ".join(item["skills"]),
            ])
        )
        for item in RESUME_FACTS
    ]


_CORPUS = _build_corpus()
_BM25 = BM25Okapi(_CORPUS)


def search_resume_facts(query: str, language: Language, limit: int = 3) -> list[EvidenceCard]:
    tokens = _tokenize(query)
    scores = _BM25.get_scores(tokens)
    ranked = sorted(range(len(RESUME_FACTS)), key=lambda i: scores[i], reverse=True)
    top = [RESUME_FACTS[i] for i in ranked if scores[i] > 0][:limit]
    if not top:
        top = RESUME_FACTS[:2]
    return [_to_evidence_card(item, language) for item in top]


def get_project_detail(project_id: str, language: Language) -> EvidenceCard | None:
    for item in RESUME_FACTS:
        if item["id"] == project_id:
            return _to_evidence_card(item, language)
    return None


def list_capabilities() -> dict[str, list[str]]:
    capabilities: dict[str, set[str]] = {}
    for item in RESUME_FACTS:
        for skill in item["skills"]:
            capabilities.setdefault(skill, set()).add(str(item["title"]))
    return {skill: sorted(projects) for skill, projects in sorted(capabilities.items())}


def execute_tool(name: str, arguments: dict[str, Any], language: Language) -> Any:
    if name == "search_resume_facts":
        return search_resume_facts(str(arguments.get("query", "")), language)
    if name == "get_project_detail":
        return get_project_detail(str(arguments.get("project_id", "")), language)
    if name == "list_capabilities":
        return list_capabilities()
    raise ValueError(f"Unsupported tool: {name}")


def serialize_tool_result(result: Any) -> Any:
    if isinstance(result, EvidenceCard):
        return result.model_dump()
    if isinstance(result, list):
        return [item.model_dump() if isinstance(item, EvidenceCard) else item for item in result]
    return result


def _to_evidence_card(item: dict[str, object], language: Language) -> EvidenceCard:
    summary_key = "summary_zh" if language == "zh" else "summary_en"
    return EvidenceCard(
        id=str(item["id"]),
        title=str(item["title"]),
        company=str(item["company"]),
        summary=str(item[summary_key]),
        evidence=list(item["evidence"]),
        skills=list(item["skills"]),
    )

