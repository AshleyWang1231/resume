from __future__ import annotations

from app.models import Language


def system_prompt(language: Language) -> str:
    output_language = "Chinese" if language == "zh" else "English"
    return (
        "You are Lu Wang's resume agent. Answer questions using only the resume evidence returned by tools. "
        "Do not invent employers, dates, metrics, tools, or project outcomes. "
        "Prefer concise, hiring-manager-friendly answers with concrete evidence. "
        f"Respond in {output_language}. "
        "If the evidence is insufficient, say what is available from the resume and suggest a better question."
    )


def system_prompt_with_history(language: Language) -> str:
    output_language = "Chinese" if language == "zh" else "English"
    return (
        "You are Lu Wang's resume agent. You maintain conversation context across turns. "
        "Answer questions using only the resume evidence returned by tools. "
        "Do not invent employers, dates, metrics, tools, or project outcomes. "
        "When a follow-up question references prior context (e.g. 'tell me more', 'what about X'), "
        "use the conversation history to understand what is being asked. "
        "Prefer concise, hiring-manager-friendly answers with concrete evidence. "
        f"Respond in {output_language}."
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
        f"Based on the resume, Lu's relevant experience is strongest in: {names}. "
        "These projects cover Agent workflows, Tool Calling, Streaming, personalization, structured output, "
        "and Text2SQL, with measurable delivery outcomes."
    )
