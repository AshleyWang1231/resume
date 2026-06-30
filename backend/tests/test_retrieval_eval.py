"""RAG retrieval evaluation — deterministic precision/recall/MRR metrics.

No LLM calls, no network. Safe to run in CI and local dev.
Tests BM25 search quality against a manually-curated gold-standard query set.
"""
from __future__ import annotations

import re
from typing import Any

import pytest

# ---------------------------------------------------------------------------
# Gold-standard test cases: (query, language, expected_doc_ids)
# expected_doc_ids = set of RESUME_FACTS ids that MUST appear in top-3 results
# ---------------------------------------------------------------------------
GOLD = [
    # Streaming / Agent Runtime
    ("what is Lu's streaming experience", "en", {"agent-runtime"}),
    ("TTFT latency optimization streaming", "en", {"agent-runtime"}),
    ("Streaming 响应架构", "zh", {"agent-runtime"}),
    # Personalization / warm-up
    ("personalization cold start warm-up cache", "en", {"personalization"}),
    ("用户画像缓存 warm-up", "zh", {"personalization"}),
    ("profile service cache layer TTL", "en", {"personalization"}),
    # Product comparison
    ("product comparison skill multi-turn", "en", {"product-comparison"}),
    ("商品对比 结构化输出", "zh", {"product-comparison"}),
    # Text2SQL
    ("Text2SQL SQL generation bank agent", "en", {"text2sql"}),
    ("意图澄清 SQL 生成 重试", "zh", {"text2sql"}),
    ("dual-layer reranking field value vector", "en", {"text2sql"}),
    # RAG chatbot
    ("RAG LlamaIndex FAISS document retrieval", "en", {"rag-chatbot"}),
    ("RAGAS evaluation answer relevance", "en", {"rag-chatbot"}),
    # Pricing system / backend
    ("Hexagonal architecture DDD Java pricing", "en", {"pricing-system"}),
    ("六边形架构 报表 MySQL", "zh", {"pricing-system"}),
    # Profile / general
    ("AI software engineer background overview", "en", {"profile"}),
    ("汪露工作经历 简介", "zh", {"profile"}),
    # Multi-hit queries (both ids must be present)
    ("agent workflow tool calling", "en", {"agent-runtime", "profile"}),
    ("evaluation test cases accuracy", "en", {"text2sql", "personalization"}),
]

K = 3  # precision/recall at K


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+|[一-鿿]", text.lower())


def _get_results(query: str, language: str, limit: int = K) -> list[str]:
    """Returns list of doc ids in ranked order."""
    import sys
    sys.path.insert(0, "src")
    from app.harness.tools import search_resume_facts
    cards = search_resume_facts(query, language, limit=limit)  # type: ignore[arg-type]
    return [c.id for c in cards if c.id]


# ---------------------------------------------------------------------------
# Metrics helpers
# ---------------------------------------------------------------------------

def precision_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    top_k = retrieved[:k]
    hits = sum(1 for doc in top_k if doc in relevant)
    return hits / k if k else 0.0


def recall_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    top_k = retrieved[:k]
    hits = sum(1 for doc in top_k if doc in relevant)
    return hits / len(relevant) if relevant else 0.0


def reciprocal_rank(retrieved: list[str], relevant: set[str]) -> float:
    for rank, doc in enumerate(retrieved, start=1):
        if doc in relevant:
            return 1.0 / rank
    return 0.0


# ---------------------------------------------------------------------------
# Pytest parametrized tests (run individually, easy to debug)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("query,language,expected_ids", GOLD)
def test_retrieval_hits_expected(query: str, language: str, expected_ids: set[str]) -> None:
    """At least one expected doc must appear in top-K results."""
    results = _get_results(query, language)
    hit = bool(set(results) & expected_ids)
    assert hit, (
        f"Query: {query!r} | expected any of {expected_ids} in top-{K}, "
        f"got: {results}"
    )


# ---------------------------------------------------------------------------
# Aggregate metrics report (not a pytest test, run directly)
# ---------------------------------------------------------------------------

def evaluate_all() -> dict[str, Any]:
    precisions, recalls, rrs = [], [], []

    print(f"\n{'Query':<45} {'Lang':<5} {'Expected':<20} {'Got':<30} P@{K}  R@{K}  RR")
    print("-" * 120)

    for query, language, expected_ids in GOLD:
        results = _get_results(query, language)
        p = precision_at_k(results, expected_ids, K)
        r = recall_at_k(results, expected_ids, K)
        rr = reciprocal_rank(results, expected_ids)
        precisions.append(p)
        recalls.append(r)
        rrs.append(rr)

        got_str = ", ".join(results[:K])
        exp_str = ", ".join(sorted(expected_ids))
        hit_mark = "✓" if r > 0 else "✗"
        print(f"{hit_mark} {query[:43]:<45} {language:<5} {exp_str:<20} {got_str:<30} {p:.2f}  {r:.2f}  {rr:.2f}")

    map_score = sum(rrs) / len(rrs)
    mean_p = sum(precisions) / len(precisions)
    mean_r = sum(recalls) / len(recalls)

    print("\n" + "=" * 60)
    print(f"Queries evaluated : {len(GOLD)}")
    print(f"Mean Precision@{K}  : {mean_p:.3f}")
    print(f"Mean Recall@{K}     : {mean_r:.3f}")
    print(f"MAP (MRR)         : {map_score:.3f}")
    hits = sum(1 for r in recalls if r > 0)
    print(f"Hit rate          : {hits}/{len(GOLD)} = {hits/len(GOLD):.1%}")
    print("=" * 60)

    return {
        "n_queries": len(GOLD),
        "mean_precision_at_k": round(mean_p, 3),
        "mean_recall_at_k": round(mean_r, 3),
        "mrr": round(map_score, 3),
        "hit_rate": round(hits / len(GOLD), 3),
    }


if __name__ == "__main__":
    metrics = evaluate_all()
