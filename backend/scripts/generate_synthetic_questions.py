#!/usr/bin/env python3
"""Synthetic question generator — RAGAS-inspired reverse engineering.

Reads RESUME_FACTS, calls an LLM to generate realistic recruiter questions
for each fact, and writes them to tests/synthetic_gold.json.

Usage:
    cd backend
    AI_PROVIDER=qwen QWEN_API_KEY=sk-... uv run python scripts/generate_synthetic_questions.py

    # or with DeepSeek:
    AI_PROVIDER=deepseek DEEPSEEK_API_KEY=sk-... uv run python scripts/generate_synthetic_questions.py

Output format (tests/synthetic_gold.json):
    [
      {
        "id": "personalization_en_0",
        "source_fact_id": "personalization",
        "query": "...",
        "language": "en",
        "expected_doc_ids": ["personalization"]
      },
      ...
    ]

Re-run to refresh the file; existing content is overwritten.
"""
from __future__ import annotations

import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from app.resume_loader import build_resume_facts

# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

_SYSTEM_EN = (
    "You are a technical recruiter evaluating a software engineer's resume. "
    "Given a resume fact, generate realistic questions a recruiter might ask. "
    "Output ONLY a JSON array of strings — no explanation, no markdown."
)

_SYSTEM_ZH = (
    "你是一位技术招聘官，正在评估一份软件工程师的简历。"
    "根据所给的简历内容，生成招聘官可能提问的真实问题。"
    "仅输出 JSON 字符串数组，不要任何解释或 Markdown。"
)

_USER_TEMPLATE_EN = """Resume fact:
Title: {title}
Company: {company}
Summary: {summary}
Key evidence: {evidence}

Generate 4 questions:
- 2 specific (ask about a concrete metric, technology, or decision)
- 1 multi-topic (reference 2 skills or outcomes from this fact)
- 1 follow-up (something a recruiter would naturally ask next)

Return as a JSON array of 4 strings."""

_USER_TEMPLATE_ZH = """简历条目：
标题：{title}
公司：{company}
内容：{summary}
关键成果：{evidence}

生成 4 个问题：
- 2 个具体问题（涉及某个指标、技术或决策）
- 1 个综合问题（引用该条目中的 2 个技能或结果）
- 1 个追问（招聘官自然会接着问的问题）

以 JSON 字符串数组形式返回（4 个字符串）。"""


# ---------------------------------------------------------------------------
# LLM call
# ---------------------------------------------------------------------------

async def _call_llm(system: str, user: str) -> list[str]:
    """Make a raw OpenAI-compatible chat completions call, return parsed list."""
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
        raise RuntimeError(f"No API key found for provider={provider}")

    import httpx

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.7,
        "max_tokens": 512,
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

    # Strip markdown code fences if model wraps output
    if content.startswith("```"):
        lines = content.splitlines()
        content = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])

    return json.loads(content)


# ---------------------------------------------------------------------------
# Main generation loop
# ---------------------------------------------------------------------------

async def generate() -> list[dict]:
    facts = build_resume_facts()
    results: list[dict] = []

    for fact in facts:
        fact_id = str(fact["id"])
        title = str(fact["title"])
        company = str(fact["company"])
        evidence_str = ", ".join(str(e) for e in fact["evidence"][:4])

        print(f"  [{fact_id}] generating EN questions ...", flush=True)
        try:
            en_questions = await _call_llm(
                _SYSTEM_EN,
                _USER_TEMPLATE_EN.format(
                    title=title,
                    company=company,
                    summary=str(fact["summary_en"])[:600],
                    evidence=evidence_str,
                ),
            )
        except Exception as exc:
            print(f"    WARN: EN failed for {fact_id}: {exc}")
            en_questions = []

        print(f"  [{fact_id}] generating ZH questions ...", flush=True)
        try:
            zh_questions = await _call_llm(
                _SYSTEM_ZH,
                _USER_TEMPLATE_ZH.format(
                    title=title,
                    company=company,
                    summary=str(fact["summary_zh"])[:600],
                    evidence=evidence_str,
                ),
            )
        except Exception as exc:
            print(f"    WARN: ZH failed for {fact_id}: {exc}")
            zh_questions = []

        for i, q in enumerate(en_questions):
            results.append({
                "id": f"{fact_id}_en_{i}",
                "source_fact_id": fact_id,
                "query": str(q).strip(),
                "language": "en",
                "expected_doc_ids": [fact_id],
            })

        for i, q in enumerate(zh_questions):
            results.append({
                "id": f"{fact_id}_zh_{i}",
                "source_fact_id": fact_id,
                "query": str(q).strip(),
                "language": "zh",
                "expected_doc_ids": [fact_id],
            })

    return results


def main() -> None:
    out_path = os.path.join(os.path.dirname(__file__), "..", "tests", "synthetic_gold.json")
    out_path = os.path.abspath(out_path)

    print(f"Generating synthetic questions for {len(build_resume_facts())} facts ...")
    results = asyncio.run(generate())
    print(f"\nGenerated {len(results)} questions total.")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Saved to {out_path}")

    # Print a sample
    print("\nSample (first 4):")
    for item in results[:4]:
        print(f"  [{item['language']}] {item['query']}")


if __name__ == "__main__":
    main()
