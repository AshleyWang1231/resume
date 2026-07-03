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
                "Summarise why I am a strong fit. "
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
                "The user wants specific numbers. "
                "State each metric in a separate sentence: project name first, then the number and what it measures. "
                "Do not group metrics into a single run-on sentence."
            ),
        )

    # Work history / career timeline — before project_detail to take priority over "经历"
    if any(t in query for t in (
        "work history", "employment", "career", "employer", "where have you worked",
        "worked at", "work at", "how long have you", "years of experience",
        "工作经历", "职业", "工作过", "任职", "工作了多久",
    )):
        return IntentResult(
            intent="work_history",
            retrieval_hint=["profile"],
            retrieval_limit=3,
            prompt_focus=(
                "The user is asking about work history or career timeline. "
                "List ALL employers with their dates from the evidence — do not omit any."
            ),
        )

    # Skills / tech stack — before project_detail to avoid falling to experience_lookup
    if any(t in query for t in (
        "skill", "tech stack", "proficient", "expertise",
        "技能", "技术栈", "擅长", "会什么", "会哪些",
    )):
        return IntentResult(
            intent="skills_lookup",
            retrieval_hint=["profile"],
            retrieval_limit=3,
            prompt_focus=(
                "The user is asking about technical skills or capabilities. "
                "Cover the full breadth of skills mentioned in the evidence."
            ),
        )

    # Evaluation / testing / quality measurement
    if any(t in query for t in (
        "evaluat", "eval case", "eval suite", "assessment", "test suite", "test case", "benchmark", "measure",
        "ragas", "faithfulness", "recall", "precision", "mrr", "judge",
        "评估", "测试集", "基准", "质量", "准确率", "召回", "检索评估",
    )):
        return IntentResult(
            intent="evaluation",
            retrieval_hint=["rag-chatbot", "text2sql", "personalization"],
            retrieval_limit=3,
            prompt_focus=(
                "The user is asking about evaluation methodology or test suites. "
                "Cover both the RAG evaluation work (RAGAS, faithfulness, context recall) "
                "and the Text2SQL evaluation suite (1,000+ cases, accuracy improvement). "
                "Mention concrete metrics where available."
            ),
        )

    # Project deep-dive
    if any(t in query for t in ("project", "detail", "项目", "经历", "experience", "built", "designed", "implemented")):
        return IntentResult(
            intent="project_detail",
            retrieval_hint=[],          # let retrieval decide
            retrieval_limit=3,
            prompt_focus=(
                "Structure the answer as three prose sentences: "
                "one for the problem, one for the approach, one for the measurable result. "
                "Do not use headers or bullet points."
            ),
        )

    # Education / graduation / degree questions
    if any(t in query for t in (
        "graduate", "graduation", "degree", "education", "university", "college",
        "study", "studied", "school", "bachelor", "master", "msc", "ba ",
        "cardiff", "engineering science", "computing",
        "毕业", "学历", "学校", "大学", "学位", "硕士", "本科", "读书", "专业",
        "卡迪夫", "工程技术大学",
    )):
        return IntentResult(
            intent="education",
            retrieval_hint=["profile"],
            retrieval_limit=2,
            prompt_focus=(
                "The user is asking about education. "
                "Mention only the highest degree: MSc Computing, Cardiff University UK (2019–2021). "
                "Only include the undergraduate degree (BA Marketing, Shanghai University of Engineering Science) "
                "if the question explicitly asks about bachelor's, undergraduate, or a second degree."
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
