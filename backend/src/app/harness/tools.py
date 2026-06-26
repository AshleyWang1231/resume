from __future__ import annotations

from typing import Any

from app.models import EvidenceCard, Language
from app.resume_data import RESUME_FACTS


def search_resume_facts(query: str, language: Language, limit: int = 3) -> list[EvidenceCard]:
    matches = _find_matches(query)
    if not matches:
        matches = RESUME_FACTS[:2]
    return [_to_evidence_card(item, language) for item in matches[:limit]]


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


def _find_matches(message: str) -> list[dict[str, object]]:
    query = message.lower()
    scored: list[tuple[int, dict[str, object]]] = []
    for item in RESUME_FACTS:
        score = sum(1 for keyword in item["keywords"] if keyword in query)
        if score:
            scored.append((score, item))
    return [item for _, item in sorted(scored, key=lambda pair: pair[0], reverse=True)]


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

