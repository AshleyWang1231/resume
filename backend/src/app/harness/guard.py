# Layer 6 — Constraints, Validation & Failure Recovery
"""Rule-based input guard — zero extra API calls.

Checks run in order; first match wins. Each check is a plain function so
they are trivially testable and easy to extend.
"""
from __future__ import annotations

import re
from dataclasses import dataclass


# ── Tuneable limits ──────────────────────────────────────────────────────────
_MAX_CHARS = 500          # Pydantic model already enforces this; belt-and-suspenders
_MIN_CHARS = 1

# ── Prompt-injection / jailbreak patterns ────────────────────────────────────
# Matches the most common injection openers (case-insensitive).
_INJECTION_RE = re.compile(
    r"ignore\s+(all\s+)?(previous|above|prior)\s+(instructions?|prompts?|context)"
    r"|forget\s+(everything|all|your\s+instructions?)"
    r"|you\s+are\s+now\s+(a|an)\s+\w+"   # "you are now a DAN"
    r"|act\s+as\s+(if\s+you\s+are\s+|a\s+|an\s+)?\w+"
    r"|pretend\s+(you\s+are|to\s+be)"
    r"|disregard\s+(your|all|the)\s+(previous|instructions?|rules?|guidelines?)"
    r"|你(现在|从现在起)?(是|扮演|假装|忘记).{0,20}(助手|ai|机器人|角色)"
    r"|忽略(之前|前面|上面|所有)(的)?(指令|提示|规则|限制)",
    re.IGNORECASE,
)

# ── Off-topic detection ───────────────────────────────────────────────────────
# If NONE of these tokens appear as whole words/subwords, the message is off-topic.
# We use regex word-boundary matching for short tokens to avoid false positives
# (e.g. "ml" inside "Hamlet", "ai" inside "sailing").
_RESUME_TOKENS_EXACT = {
    # Short tokens (≤ 4 chars) that need word-boundary protection to avoid
    # false positives: "ai" in "sailing", "ml" in "Hamlet", "api" in "capital"
    "ai", "ml", "cv", "lu", "api", "rag", "sql", "ttft",
}
_RESUME_TOKENS_SUBSTR = {
    # Longer tokens — substring match is reliable
    "agent", "agents", "llm", "model", "stream", "streaming",
    "tool", "calling", "text2sql", "vector", "embedding",
    "faiss", "retrieval", "rerank", "python", "java", "fastapi", "redis",
    "zalando", "thoughtworks", "bank", "experience", "project", "skill",
    "work", "role", "resume", "hire", "hiring", "engineer",
    "engineering", "backend", "system", "design", "architect",
    "performance", "latency", "cache", "async", "impact", "metric",
    "accuracy", "eval", "evaluation", "personali", "recommend", "wang",
    # Chinese
    "工程", "项目", "经验", "技能", "简历", "后端", "系统", "架构", "模型",
    "工具", "检索", "向量", "嵌入", "流式", "推荐", "个性化", "优化", "延迟",
    "评估", "准确", "指标", "银行", "购物", "导购", "汪露",
    # Work / career context
    "工作", "职位", "职业", "公司", "就职", "入职", "在职", "任职",
    "career", "company", "position", "employer", "employment",
}

_RESUME_EXACT_RE = re.compile(
    r"\b(" + "|".join(re.escape(t) for t in sorted(_RESUME_TOKENS_EXACT, key=len, reverse=True)) + r")\b",
    re.IGNORECASE,
)

# ── Education / background questions not in resume ───────────────────────────
_EDUCATION_RE = re.compile(
    r"学校|大学|毕业|学历|本科|硕士|博士|学位|专业|院校"
    r"|university|college|degree|education|graduated|major|school",
    re.IGNORECASE,
)



_GREETINGS = {
    "hello", "hi", "hey", "hiya", "yo", "sup",
    "你好", "嗨", "哈喽", "您好", "hello!", "hi!",
}

# Very short questions (≤ 3 words) are usually navigation commands — allow them through
_SHORT_MSG_WORD_THRESHOLD = 3


@dataclass(frozen=True)
class GuardResult:
    ok: bool
    reason: str = ""       # populated only when ok=False; used for logging
    reply_en: str = ""     # fixed reply shown to user when ok=False
    reply_zh: str = ""


# ── Public API ───────────────────────────────────────────────────────────────

def guard(message: str) -> GuardResult:
    """Return GuardResult(ok=True) to allow, GuardResult(ok=False) to block."""
    text = message.strip()

    result = _check_length(text)
    if result is not None:
        return result

    result = _check_greeting(text)
    if result is not None:
        return result

    result = _check_education(text)
    if result is not None:
        return result

    result = _check_injection(text)
    if result is not None:
        return result

    result = _check_off_topic(text)
    if result is not None:
        return result

    return GuardResult(ok=True)


# ── Individual checks ─────────────────────────────────────────────────────────

def _check_length(text: str) -> GuardResult | None:
    if len(text) < _MIN_CHARS:
        return GuardResult(
            ok=False,
            reason="empty_message",
            reply_en="Please enter a question.",
            reply_zh="请输入问题。",
        )
    if len(text) > _MAX_CHARS:
        return GuardResult(
            ok=False,
            reason="message_too_long",
            reply_en="Your message is too long. Please keep it under 500 characters.",
            reply_zh="消息过长，请控制在 500 字以内。",
        )
    return None


def _check_education(text: str) -> GuardResult | None:
    if _EDUCATION_RE.search(text):
        return GuardResult(
            ok=False,
            reason="education_not_available",
            reply_en="Lu Wang's resume focuses on professional experience rather than education background. Feel free to ask about her AI engineering work at Zalando or Thoughtworks.",
            reply_zh="汪露的简历以工作经验为主，未包含学历信息。欢迎询问她在 Zalando 或 Thoughtworks 的 AI 工程经历。",
        )
    return None


def _check_greeting(text: str) -> GuardResult | None:
    if text.lower().strip("!? ") in _GREETINGS:
        return GuardResult(
            ok=False,
            reason="greeting",
            reply_en="Hi! I'm Lu Wang's resume agent. Ask me about her Agent Runtime work at Zalando, Text2SQL pipeline, or Streaming architecture.",
            reply_zh="你好！我是汪露的简历 Agent。可以问我她在 Zalando 的 Agent Runtime 工作、Text2SQL 流水线或 Streaming 架构。",
        )
    return None


def _check_injection(text: str) -> GuardResult | None:
    if _INJECTION_RE.search(text):
        return GuardResult(
            ok=False,
            reason="prompt_injection",
            reply_en="I can only answer questions about Lu Wang's resume and experience.",
            reply_zh="我只能回答关于汪露简历和工作经验的问题。",
        )
    return None


def _check_off_topic(text: str) -> GuardResult | None:
    # Slash commands (/projects, /capabilities, …) always pass
    if text.startswith("/"):
        return None

    lower = text.lower()
    # Check word-boundary tokens first
    if _RESUME_EXACT_RE.search(lower):
        return None
    # Then substring tokens
    if any(token in lower for token in _RESUME_TOKENS_SUBSTR):
        return None

    # Allow very short follow-up phrases that lack resume keywords but make
    # sense in multi-turn context: "tell me more", "what else", "ok thanks" etc.
    words = text.split()
    if len(words) <= _SHORT_MSG_WORD_THRESHOLD:
        _FOLLOWUP_RE = re.compile(
            r"\b(more|else|what|why|how|who|when|which|tell|show|explain|describe"
            r"|continue|go on|next|thanks|ok|sure|got it|yes|no|和|什么|怎么|为什么|继续)\b",
            re.IGNORECASE,
        )
        if _FOLLOWUP_RE.search(lower):
            return None
        # Pure noise (abc, xyz, random chars) — treat as off-topic
        return GuardResult(
            ok=False,
            reason="off_topic",
            reply_en=(
                "This agent is focused on Lu Wang's resume. "
                "Try asking about projects, skills, or experience."
            ),
            reply_zh=(
                "这个 Agent 专注于汪露的简历内容。"
                "可以询问项目、技能或工作经验。"
            ),
        )

    return GuardResult(
        ok=False,
        reason="off_topic",
        reply_en=(
            "This agent is focused on Lu Wang's resume. "
            "Try asking about projects, skills, or experience."
        ),
        reply_zh=(
            "这个 Agent 专注于汪露的简历内容。"
            "可以询问项目、技能或工作经验。"
        ),
    )
