"""LLM-as-judge evaluation — faithfulness + answer relevance.

Inspired by RAGAS: rather than hand-writing keyword assertions, use an LLM
to score answer quality on two axes:

  faithfulness     — does the answer stay grounded in the evidence?
                     (does it invent facts not present in the evidence cards?)
  answer_relevance — does the answer actually address the question asked?

Gate: only runs when JUDGE_EVAL=1 is set.  This prevents expensive LLM calls
in normal CI.  Run manually or in a dedicated eval workflow:

    cd backend
    JUDGE_EVAL=1 AI_PROVIDER=qwen QWEN_API_KEY=sk-... \\
        uv run pytest tests/test_llm_judge_eval.py -v

Each test case includes:
  - message + language  (input to the resume agent)
  - min_faithfulness    (0.0–1.0 threshold to pass)
  - min_relevance       (0.0–1.0 threshold to pass)

Scoring:
  Both metrics are 0.0 / 0.5 / 1.0 from the judge LLM.
  A test passes when both scores meet their thresholds.
"""
from __future__ import annotations

import asyncio
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# Skip all tests in this module unless explicitly opted in
pytestmark = pytest.mark.skipif(
    os.getenv("JUDGE_EVAL") != "1",
    reason="JUDGE_EVAL=1 required — skipped in normal CI",
)

# ---------------------------------------------------------------------------
# Eval cases: (message, language, min_faithfulness, min_relevance)
# ---------------------------------------------------------------------------

JUDGE_CASES = [
    {
        "id": "streaming_en",
        "message": "What did Lu do to improve streaming latency at Zalando?",
        "language": "en",
        "min_faithfulness": 0.8,
        "min_relevance": 0.8,
    },
    {
        "id": "personalization_zh",
        "message": "汪露是怎么解决首屏冷启动问题的？",
        "language": "zh",
        "min_faithfulness": 0.8,
        "min_relevance": 0.8,
    },
    {
        "id": "text2sql_accuracy",
        "message": "How did Lu improve the accuracy of the Text2SQL agent?",
        "language": "en",
        "min_faithfulness": 0.8,
        "min_relevance": 0.8,
    },
    {
        "id": "product_comparison_zh",
        "message": "商品对比功能是怎么做到多轮引用的？",
        "language": "zh",
        "min_faithfulness": 0.8,
        "min_relevance": 0.8,
    },
    {
        "id": "hallucination_probe_en",
        "message": "What is Lu's experience with Kubernetes and LangChain?",
        "language": "en",
        "min_faithfulness": 0.8,   # should NOT invent Kubernetes/LangChain claims
        "min_relevance": 0.5,      # relevance lower — question is about absent topics
    },
    {
        "id": "profile_overview_zh",
        "message": "汪露的整体背景和技术方向是什么？",
        "language": "zh",
        "min_faithfulness": 0.8,
        "min_relevance": 0.8,
    },
    {
        "id": "rag_experience_en",
        "message": "Describe Lu's experience with RAG pipelines and evaluation.",
        "language": "en",
        "min_faithfulness": 0.8,
        "min_relevance": 0.8,
    },
    {
        "id": "pricing_backend_en",
        "message": "What backend work did Lu do for the bank pricing system?",
        "language": "en",
        "min_faithfulness": 0.8,
        "min_relevance": 0.8,
    },
]


# ---------------------------------------------------------------------------
# Judge prompts
# ---------------------------------------------------------------------------

_FAITHFULNESS_SYSTEM = (
    "You are an impartial evaluator assessing whether an AI answer is grounded "
    "in the provided evidence. Score faithfulness as:\n"
    "  1.0 — all factual claims are supported by evidence\n"
    "  0.5 — some minor claims lack evidence, but no clear fabrications\n"
    "  0.0 — the answer contains facts clearly absent from the evidence\n\n"
    "Return ONLY a JSON object: {\"score\": <number>, \"reason\": \"<one sentence>\"}"
)

_RELEVANCE_SYSTEM = (
    "You are an impartial evaluator assessing whether an AI answer actually "
    "addresses the user's question. Score answer relevance as:\n"
    "  1.0 — fully answers the question\n"
    "  0.5 — partially answers; misses some important aspect\n"
    "  0.0 — does not answer the question, or is completely off-topic\n\n"
    "Return ONLY a JSON object: {\"score\": <number>, \"reason\": \"<one sentence>\"}"
)


def _faithfulness_user(question: str, evidence: list[dict], answer: str) -> str:
    ev_text = "\n\n".join(
        f"[{e.get('title', '')} @ {e.get('company', '')}]\n{e.get('summary', '')}"
        for e in evidence
    )
    return (
        f"Question: {question}\n\n"
        f"Evidence provided to the AI:\n{ev_text}\n\n"
        f"AI answer:\n{answer}\n\n"
        "Score faithfulness (1.0 / 0.5 / 0.0)."
    )


def _relevance_user(question: str, answer: str) -> str:
    return (
        f"Question: {question}\n\n"
        f"AI answer:\n{answer}\n\n"
        "Score answer relevance (1.0 / 0.5 / 0.0)."
    )


# ---------------------------------------------------------------------------
# LLM judge call
# ---------------------------------------------------------------------------

async def _judge(system: str, user: str) -> dict:
    """Call the judge LLM; returns {"score": float, "reason": str}."""
    provider = os.getenv("AI_PROVIDER", "deepseek").lower()

    if provider == "qwen":
        api_key = os.getenv("QWEN_API_KEY") or os.getenv("DASHSCOPE_API_KEY") or ""
        base_url = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
        model = os.getenv("QWEN_MODEL", "qwen-turbo")
    elif provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY") or ""
        base_url = "https://api.openai.com/v1"
        model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    else:  # deepseek
        api_key = os.getenv("DEEPSEEK_API_KEY") or ""
        base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        model = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash")

    if not api_key:
        pytest.skip(f"No API key for provider={provider}")

    import httpx

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.0,
        "max_tokens": 256,
    }
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{base_url.rstrip('/')}/chat/completions",
            headers={"authorization": f"Bearer {api_key}", "content-type": "application/json"},
            content=json.dumps(payload).encode(),
        )
        resp.raise_for_status()
        data = resp.json()

    content = data["choices"][0]["message"]["content"].strip()
    if content.startswith("```"):
        lines = content.splitlines()
        content = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])

    return json.loads(content)


# ---------------------------------------------------------------------------
# Agent runner
# ---------------------------------------------------------------------------

async def _get_agent_response(message: str, language: str) -> tuple[str, list[dict]]:
    """Run the agent and return (answer_text, evidence_dicts)."""
    from app.harness.agent import ResumeAgent
    from app.models import ChatRequest

    response = await ResumeAgent().answer(ChatRequest(message=message, language=language))
    evidence_dicts = [e.model_dump() for e in response.evidence]
    return response.answer, evidence_dicts


# ---------------------------------------------------------------------------
# Pytest parametrized tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("case", JUDGE_CASES, ids=[c["id"] for c in JUDGE_CASES])
def test_faithfulness(case: dict) -> None:
    answer, evidence = asyncio.run(_get_agent_response(case["message"], case["language"]))
    assert answer, f"Agent returned empty answer for: {case['message']}"

    result = asyncio.run(_judge(
        _FAITHFULNESS_SYSTEM,
        _faithfulness_user(case["message"], evidence, answer),
    ))
    score = float(result.get("score", 0))
    reason = result.get("reason", "")

    print(f"\n  faithfulness={score:.1f} | {reason}")
    assert score >= case["min_faithfulness"], (
        f"Faithfulness {score:.1f} < {case['min_faithfulness']} | {reason}\n"
        f"Answer: {answer[:300]}"
    )


@pytest.mark.parametrize("case", JUDGE_CASES, ids=[c["id"] for c in JUDGE_CASES])
def test_answer_relevance(case: dict) -> None:
    answer, _ = asyncio.run(_get_agent_response(case["message"], case["language"]))
    assert answer, f"Agent returned empty answer for: {case['message']}"

    result = asyncio.run(_judge(
        _RELEVANCE_SYSTEM,
        _relevance_user(case["message"], answer),
    ))
    score = float(result.get("score", 0))
    reason = result.get("reason", "")

    print(f"\n  relevance={score:.1f} | {reason}")
    assert score >= case["min_relevance"], (
        f"Relevance {score:.1f} < {case['min_relevance']} | {reason}\n"
        f"Answer: {answer[:300]}"
    )


# ---------------------------------------------------------------------------
# Aggregate report (run directly)
# ---------------------------------------------------------------------------

def evaluate_all() -> None:
    """Print a full faithfulness + relevance report for all cases."""
    print(f"\n{'ID':<30} {'F@score':<10} {'R@score':<10} {'Faithfulness reason':<50} {'Relevance reason'}")
    print("-" * 140)

    f_scores, r_scores = [], []
    for case in JUDGE_CASES:
        answer, evidence = asyncio.run(_get_agent_response(case["message"], case["language"]))
        if not answer:
            print(f"{case['id']:<30} NO ANSWER")
            continue

        f_result = asyncio.run(_judge(_FAITHFULNESS_SYSTEM, _faithfulness_user(case["message"], evidence, answer)))
        r_result = asyncio.run(_judge(_RELEVANCE_SYSTEM, _relevance_user(case["message"], answer)))

        fs = float(f_result.get("score", 0))
        rs = float(r_result.get("score", 0))
        f_scores.append(fs)
        r_scores.append(rs)

        f_ok = "✓" if fs >= case["min_faithfulness"] else "✗"
        r_ok = "✓" if rs >= case["min_relevance"] else "✗"
        print(
            f"{f_ok}{r_ok} {case['id']:<28} {fs:<10.1f} {rs:<10.1f} "
            f"{f_result.get('reason', '')[:48]:<50} {r_result.get('reason', '')[:50]}"
        )

    if f_scores:
        print("\n" + "=" * 60)
        print(f"Cases evaluated     : {len(f_scores)}")
        print(f"Mean faithfulness   : {sum(f_scores)/len(f_scores):.3f}")
        print(f"Mean relevance      : {sum(r_scores)/len(r_scores):.3f}")
        f_pass = sum(1 for s, c in zip(f_scores, JUDGE_CASES) if s >= c["min_faithfulness"])
        r_pass = sum(1 for s, c in zip(r_scores, JUDGE_CASES) if s >= c["min_relevance"])
        print(f"Faithfulness pass   : {f_pass}/{len(f_scores)}")
        print(f"Relevance pass      : {r_pass}/{len(r_scores)}")
        print("=" * 60)


if __name__ == "__main__":
    evaluate_all()
