from __future__ import annotations

import re
from typing import Any

try:
    from rank_bm25 import BM25Okapi as _BM25Okapi
    _HAS_BM25 = True
except ImportError:
    _HAS_BM25 = False

from app.models import EvidenceCard, Language
from app.resume_data import RESUME_FACTS


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+|[一-鿿]", text.lower())


def _doc_text(item: dict[str, object]) -> str:
    return " ".join([
        str(item["id"]),
        str(item["title"]),
        str(item["summary_en"]),
        str(item["summary_zh"]),
        " ".join(item["skills"]),  # type: ignore[arg-type]
    ])


_CORPUS = [_tokenize(_doc_text(item)) for item in RESUME_FACTS]
_BM25 = _BM25Okapi(_CORPUS) if _HAS_BM25 else None


def search_resume_facts(query: str, language: Language, limit: int = 3) -> list[EvidenceCard]:
    if _BM25 is not None:
        tokens = _tokenize(query)
        scores = _BM25.get_scores(tokens)
        ranked = [i for i in sorted(range(len(RESUME_FACTS)), key=lambda i: scores[i], reverse=True) if scores[i] > 0]
    else:
        ranked = []

    if not ranked:
        ranked = list(range(min(2, len(RESUME_FACTS))))

    return [_to_evidence_card(RESUME_FACTS[i], language) for i in ranked[:limit]]


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
        evidence=list(item["evidence"]),  # type: ignore[arg-type]
        skills=list(item["skills"]),  # type: ignore[arg-type]
    )
