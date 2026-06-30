from __future__ import annotations

import os
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

# FAISS index — built lazily on first use to avoid import cost at startup
_faiss_index = None
_faiss_ready = False


def _get_faiss_index():
    global _faiss_index, _faiss_ready
    if _faiss_ready:
        return _faiss_index

    embedding_key = os.getenv("QWEN_API_KEY") or os.getenv("DASHSCOPE_API_KEY") or os.getenv("EMBEDDING_API_KEY")
    if not embedding_key:
        _faiss_ready = True
        return None

    try:
        import faiss
        import numpy as np
        from app.harness.embedding import embed

        texts = [_doc_text(item) for item in RESUME_FACTS]
        vecs = embed(texts)
        mat = np.array(vecs, dtype="float32")
        faiss.normalize_L2(mat)
        index = faiss.IndexFlatIP(mat.shape[1])
        index.add(mat)
        _faiss_index = index
    except Exception:
        _faiss_index = None

    _faiss_ready = True
    return _faiss_index


def _rrf(rankings: list[list[int]], k: int = 60) -> list[int]:
    scores: dict[int, float] = {}
    for ranking in rankings:
        for rank, idx in enumerate(ranking):
            scores[idx] = scores.get(idx, 0.0) + 1.0 / (k + rank + 1)
    return sorted(scores, key=lambda i: scores[i], reverse=True)


def search_resume_facts(query: str, language: Language, limit: int = 3) -> list[EvidenceCard]:
    # BM25 ranking
    bm25_ranked: list[int] = []
    if _BM25 is not None:
        tokens = _tokenize(query)
        bm25_scores = _BM25.get_scores(tokens)
        bm25_ranked = [i for i in sorted(range(len(RESUME_FACTS)), key=lambda i: bm25_scores[i], reverse=True) if bm25_scores[i] > 0]

    # FAISS ranking (skip if not configured)
    faiss_index = _get_faiss_index()
    faiss_ranked: list[int] = []
    if faiss_index is not None:
        try:
            import faiss
            import numpy as np
            from app.harness.embedding import embed
            qvec = np.array(embed([query]), dtype="float32")
            faiss.normalize_L2(qvec)
            _, ids = faiss_index.search(qvec, len(RESUME_FACTS))
            faiss_ranked = [int(i) for i in ids[0] if i >= 0]
        except Exception:
            pass

    if faiss_ranked:
        fused = _rrf([bm25_ranked, faiss_ranked])
    elif bm25_ranked:
        fused = bm25_ranked
    else:
        fused = list(range(min(2, len(RESUME_FACTS))))

    return [_to_evidence_card(RESUME_FACTS[i], language) for i in fused[:limit]]


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
