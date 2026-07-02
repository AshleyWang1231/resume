# Layer 1 — Context Management (intent routing)
"""Intent routing — Layer 1 (Context Management) + Layer 3 (Execution Orchestration).

Classifies the user's message into one of five intents and attaches:
- retrieval_hint: which RESUME_FACTS ids to boost / retrieve first
- retrieval_limit: how many evidence cards to fetch (more for broad queries)
- prompt_focus: a one-sentence focus instruction injected into the system prompt
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class IntentResult:
    intent: str
    retrieval_hint: list[str] = field(default_factory=list)   # doc ids to prioritise
    retrieval_limit: int = 3
    prompt_focus: str = ""


def route_intent(message: str) -> IntentResult:
    query = message.lower()

    # Interview / behavioural questions
    if any(t in query for t in ("interview", "面试", "challenge", "conflict", "why", "weakness")):
        return IntentResult(
            intent="interview_answer",
            retrieval_hint=["profile", "agent-runtime", "personalization"],
            retrieval_limit=3,
            prompt_focus=(
                "Answer in a structured STAR-style (Situation → Action → Result). "
                "Draw on concrete project evidence."
            ),
        )

    # Job-fit / role match
    if any(t in query for t in ("fit", "match", "jd", "job", "岗位", "匹配", "suitable", "qualify")):
        return IntentResult(
            intent="role_fit",
            retrieval_hint=["profile"],
            retrieval_limit=4,
            prompt_focus=(
                "Summarise why Lu Wang is a strong fit. "
                "Map specific skills and projects to the question."
            ),
        )

    # Metrics / impact numbers
    if any(t in query for t in ("metric", "impact", "result", "量化", "指标", "成果", "number", "数字", "%", "percent")):
        return IntentResult(
            intent="impact_metrics",
            retrieval_hint=["agent-runtime", "personalization", "text2sql", "product-comparison"],
            retrieval_limit=4,
            prompt_focus=(
                "Lead with specific numbers and percentages. "
                "Always state the project context before the metric."
            ),
        )

    # Project deep-dive
    if any(t in query for t in ("project", "detail", "项目", "经历", "experience", "built", "designed", "implemented")):
        return IntentResult(
            intent="project_detail",
            retrieval_hint=[],          # let retrieval decide
            retrieval_limit=3,
            prompt_focus=(
                "Give a concise problem → approach → result narrative. "
                "Mention the specific challenge and measurable outcome."
            ),
        )

    # Broad overview / "who is Lu Wang" — must be about the person, not a specific topic
    if any(t in query for t in (
        "who is lu", "who is wang", "介绍汪露", "介绍一下汪露", "汪露是谁",
        "overview", "background", "introduce lu", "what has lu done",
        "what problems has lu", "engineering problems has lu", "engineering challenges has lu",
    )):
        return IntentResult(
            intent="overview",
            retrieval_hint=["profile"],
            retrieval_limit=2,
            prompt_focus=(
                "Give a concise 2-3 sentence overview drawing on the profile evidence. "
                "Name the two most relevant expertise areas with a concrete example each. "
                "End by inviting the user to ask about a specific project or skill."
            ),
        )

    # General experience / capability lookup (default)
    return IntentResult(
        intent="experience_lookup",
        retrieval_hint=[],
        retrieval_limit=3,
        prompt_focus="",
    )
