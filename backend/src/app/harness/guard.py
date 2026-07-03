# Layer 6 — Constraints, Validation & Failure Recovery
"""Rule-based input guard — zero extra API calls.

Checks run in order; first match wins. Each check is a plain function so
they are trivially testable and easy to extend.

Off-topic filtering is intentionally omitted: the LLM system prompt is the
semantic boundary. Only injection attacks and length violations are blocked here.
"""
from __future__ import annotations

import re
from dataclasses import dataclass


# ── Tuneable limits ──────────────────────────────────────────────────────────
_MAX_CHARS = 500          # Pydantic model already enforces this; belt-and-suspenders
_MIN_CHARS = 1

# Inputs that are too short to be a real question (digits, single letters, punctuation only)
# Also blocks pure-digit strings of any length (e.g. "666", "6666", "666!")
_MEANINGLESS_RE = re.compile(r"^[\d\s\W]{1,3}$")
_DIGITS_ONLY_RE = re.compile(r"^[\d\s\W]*\d[\d\s\W]*$")

# ── Prompt-injection / jailbreak patterns ────────────────────────────────────
_INJECTION_RE = re.compile(
    r"ignore\s+(all\s+)?(previous|above|prior)\s+(instructions?|prompts?|context)"
    r"|forget\s+(everything|all|your\s+instructions?)"
    r"|you\s+are\s+now\s+(a|an)\s+\w+"
    r"|act\s+as\s+(if\s+you\s+are\s+|a\s+|an\s+)?\w+"
    r"|pretend\s+(you\s+are|to\s+be)"
    r"|disregard\s+(your|all|the)\s+(previous|instructions?|rules?|guidelines?)"
    r"|你(现在|从现在起)?(是|扮演|假装|忘记).{0,20}(助手|ai|机器人|角色)"
    r"|忽略(之前|前面|上面|所有)(的)?(指令|提示|规则|限制)",
    re.IGNORECASE,
)

# ── Greeting detection ───────────────────────────────────────────────────────
_GREETINGS = {
    "hello", "hi", "hey", "hiya", "yo", "sup",
    "你好", "嗨", "哈喽", "您好", "hello!", "hi!",
}


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

    result = _check_meaningless(text)
    if result is not None:
        return result

    result = _check_greeting(text)
    if result is not None:
        return result

    result = _check_injection(text)
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


def _check_meaningless(text: str) -> GuardResult | None:
    if _MEANINGLESS_RE.match(text) or _DIGITS_ONLY_RE.match(text):
        return GuardResult(
            ok=False,
            reason="meaningless_input",
            reply_en="I'm Lu Wang's resume agent — ask me about her experience, projects, or skills.",
            reply_zh="我是汪露的简历 Agent，可以问我她的工作经历、项目或技能。",
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
