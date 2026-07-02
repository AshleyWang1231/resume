# Layer 1 — Context Management (prompt construction)
"""Prompt construction — Layer 1 (Context Management).

Builds system prompts that include:
- Role + identity definition
- Intent-specific focus instruction (from router.IntentResult)
- Formatting constraints
- History awareness flag
"""
from __future__ import annotations

from app.models import Language

# Import here to avoid circular; IntentResult is a plain dataclass
_FOCUS_PLACEHOLDER = ""


def _base_rules(language: Language, has_history: bool = False) -> str:
    output_language = "Chinese" if language == "zh" else "English"
    history_clause = (
        "You maintain conversation context across turns. "
        "When a follow-up references prior context (e.g. 'tell me more', 'what about X'), "
        "use the conversation history to understand what is being asked. "
        if has_history else ""
    )
    return (
        "You are the resume agent for Lu Wang (汪露), an AI Software Engineer. "
        "Lu Wang and 汪露 refer to the same person — always treat them as identical. "
        f"{history_clause}"
        "Answer questions using only the resume evidence returned by tools. "
        "Do not invent employers, dates, metrics, tools, or project outcomes. "
        "Prefer concise, hiring-manager-friendly answers with concrete evidence. "
        "Keep answers to 2-3 sentences. Lead with the specific outcome or technique, then one sentence of context. "
        "Never enumerate all projects — focus only on the single most relevant piece of evidence. "
        f"Respond in {output_language}. "
        "If the evidence is insufficient, say what IS available and suggest a better question. "
        "FORMATTING RULES (strictly enforced): "
        "1. Plain prose only — no markdown headers (###, ##, #), no bold (**text**), no bullet lists (- or *), no code blocks. "
        "2. Never wrap output in XML or HTML tags such as <error>, <answer>, <response>. "
        "3. If you cannot find relevant evidence, say so in one sentence — do not produce an error block."
    )


def system_prompt(language: Language, focus: str = "") -> str:
    base = _base_rules(language, has_history=False)
    if focus:
        base += f" FOCUS FOR THIS QUERY: {focus}"
    return base


def system_prompt_with_history(language: Language, focus: str = "") -> str:
    base = _base_rules(language, has_history=True)
    if focus:
        base += f" FOCUS FOR THIS QUERY: {focus}"
    return base


def self_check_prompt(language: Language, answer: str) -> str:
    """Prompt for the self-correction loop (Layer 3 / Layer 6).

    Asks the model to judge whether the answer is grounded and complete.
    Returns 'OK' if acceptable, or a one-sentence improvement instruction.
    """
    output_language = "Chinese" if language == "zh" else "English"
    return (
        f"You are a quality reviewer for a resume agent. Respond in {output_language}.\n\n"
        f"ANSWER TO REVIEW:\n{answer}\n\n"
        "Check ONLY these two things:\n"
        "1. Does the answer contain invented facts (employers, dates, metrics, tools not in the resume)?\n"
        "2. Is the answer completely empty or clearly off-topic?\n\n"
        "If both checks pass, reply with exactly: OK\n"
        "If a check fails, reply with one sentence starting with 'IMPROVE:' explaining what to fix. "
        "Do not rewrite the answer."
    )


def fallback_answer(language: Language, project_names: list[str]) -> str:
    if language == "zh":
        names = "、".join(project_names)
        return (
            f"根据简历，汪露的相关经验主要体现在：{names}。"
            "这些项目覆盖 Agent、Tool Calling、Streaming、个性化、结构化输出和 Text2SQL 等方向，并且包含可量化结果。"
        )
    names = ", ".join(project_names)
    return (
        f"Based on the resume, Lu Wang's relevant experience is strongest in: {names}. "
        "These projects cover Agent workflows, Tool Calling, Streaming, personalization, structured output, "
        "and Text2SQL, with measurable delivery outcomes."
    )
