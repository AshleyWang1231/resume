# Layer 3 — Execution Orchestration (Agent Runtime)
"""Agent Runtime — Layer 3 (Execution Orchestration) + Layer 4 (Memory & State).

Orchestrates the full request lifecycle:
  Guard → Intent routing → Hybrid retrieval → LLM workflow loop →
  Self-correction (max 2 retries) → Fallback → SSE stream
"""
from __future__ import annotations

import time
import uuid
from collections.abc import AsyncIterator

from app.harness.events import sse_event, _chunk_text
from app.harness.guard import guard
from app.harness.prompts import fallback_answer, self_check_prompt
from app.harness.provider_factory import LLMClient, build_llm_client
from app.harness.router import route_intent
from app.harness.stream_types import StreamEvent
from app.harness.tools import search_resume_facts
from app.harness.utils import log as _log
from app.models import AgentContext, ChatRequest, ChatResponse
from app.resume_data import SUGGESTED_QUESTIONS
from app.session import session_store

MAX_SELF_CORRECTION_ATTEMPTS = 2


class ResumeAgent:
    def __init__(self, llm_client: LLMClient | None = None) -> None:
        self.llm_client = llm_client

    # ── Non-streaming path ──────────────────────────────────────────────────

    async def answer(self, request: ChatRequest, ai_binding=None) -> ChatResponse:
        llm_client = self.llm_client or build_llm_client(ai_binding)
        session_id = request.session_id or str(uuid.uuid4())
        history = session_store.get_history(session_id)

        # Layer 1 – Context: build intent + context
        intent = route_intent(request.message)
        context = AgentContext(
            request_id=str(uuid.uuid4()),
            message=request.message.strip(),
            language=request.language,
            intent=intent.intent,
            session_id=session_id,
        )
        _log("intent_routed", request_id=context.request_id, intent=intent.intent,
             focus=intent.prompt_focus[:60] if intent.prompt_focus else "")

        # Layer 6 – Constraints: guard
        guard_result = guard(context.message)
        if not guard_result.ok:
            _log("guard_blocked", request_id=context.request_id, reason=guard_result.reason)
            reply = guard_result.reply_zh if request.language == "zh" else guard_result.reply_en
            return ChatResponse(
                answer=reply, evidence=[],
                suggested_questions=SUGGESTED_QUESTIONS[context.language],
                request_id=context.request_id, session_id=session_id,
                source="guard", tools_called=[],
            )

        # Layer 2 – Tools: hybrid retrieval with intent boosting
        seed_evidence = search_resume_facts(
            context.message, context.language,
            limit=intent.retrieval_limit,
            intent_hint=intent.retrieval_hint,
        )
        _log("retrieval_done", request_id=context.request_id,
             evidence_count=len(seed_evidence), intent=intent.intent,
             titles=[e.title for e in seed_evidence])

        if not llm_client.is_configured():
            _log("llm_not_configured", provider=llm_client.provider, request_id=context.request_id)
            return self._fallback(context, session_id, seed_evidence)

        # Layer 3 – Orchestration: LLM call + self-correction loop
        _log("llm_call_start", provider=llm_client.provider, request_id=context.request_id,
             session_id=session_id, history_turns=len(history))
        t0 = time.monotonic()
        llm_result = None
        try:
            llm_result = await llm_client.answer(
                context.message, context.language, seed_evidence,
                history=history,
                focus=intent.prompt_focus,
                intent_hint=intent.retrieval_hint,
            )
        except Exception as exc:
            _log("llm_call_error", provider=llm_client.provider, request_id=context.request_id,
                 elapsed_ms=round((time.monotonic() - t0) * 1000),
                 error_type=exc.__class__.__name__, error_message=str(exc))

        # Layer 6 – Self-correction: up to MAX_SELF_CORRECTION_ATTEMPTS retries
        if llm_result:
            llm_result = await self._self_correct(
                llm_client, llm_result, context, seed_evidence, history, t0,
            )

        elapsed_ms = round((time.monotonic() - t0) * 1000)
        _log("llm_call_done", provider=llm_client.provider if llm_result else "fallback",
             request_id=context.request_id, elapsed_ms=elapsed_ms,
             has_result=llm_result is not None)

        if llm_result:
            session_store.append(session_id, "user", context.message)
            session_store.append(session_id, "assistant", llm_result.answer)
            return ChatResponse(
                answer=llm_result.answer, evidence=llm_result.evidence,
                suggested_questions=SUGGESTED_QUESTIONS[context.language],
                request_id=context.request_id, session_id=session_id,
                source=llm_result.provider, tools_called=llm_result.tools_called,
            )

        return self._fallback(context, session_id, seed_evidence)

    # ── Streaming path ──────────────────────────────────────────────────────

    async def stream(self, request: ChatRequest, ai_binding=None) -> AsyncIterator[str]:
        llm_client = self.llm_client or build_llm_client(ai_binding)
        session_id = request.session_id or str(uuid.uuid4())
        history = session_store.get_history(session_id)

        # Layer 1 – Context: intent routing
        intent = route_intent(request.message)
        context = AgentContext(
            request_id=str(uuid.uuid4()),
            message=request.message.strip(),
            language=request.language,
            intent=intent.intent,
            session_id=session_id,
        )
        _log("intent_routed", request_id=context.request_id, intent=intent.intent)

        # Layer 6 – Constraints: guard
        guard_result = guard(context.message)
        if not guard_result.ok:
            _log("guard_blocked", request_id=context.request_id, reason=guard_result.reason)
            reply = guard_result.reply_zh if request.language == "zh" else guard_result.reply_en
            yield sse_event("metadata", {
                "request_id": context.request_id, "session_id": session_id,
                "source": "guard", "tools_called": [],
            })
            for chunk in _chunk_text(reply):
                yield sse_event("answer_delta", {"text": chunk})
            yield sse_event("evidence", [])
            yield sse_event("done", {
                "request_id": context.request_id, "session_id": session_id,
                "suggested_questions": SUGGESTED_QUESTIONS[context.language],
            })
            return

        # Layer 2 – Tools: hybrid retrieval
        seed_evidence = search_resume_facts(
            context.message, context.language,
            limit=intent.retrieval_limit,
            intent_hint=intent.retrieval_hint,
        )
        _log("retrieval_done", request_id=context.request_id,
             evidence_count=len(seed_evidence), intent=intent.intent)

        yield sse_event("metadata", {
            "request_id": context.request_id, "session_id": session_id,
            "source": llm_client.provider, "tools_called": [],
        })

        stream_fn = getattr(llm_client, "stream_answer", None)
        if not callable(stream_fn) or not llm_client.is_configured():
            _log("stream_fallback", request_id=context.request_id, provider=llm_client.provider)
            fallback_text = fallback_answer(context.language, [e.title for e in seed_evidence])
            for chunk in _chunk_text(fallback_text):
                yield sse_event("answer_delta", {"text": chunk})
            yield sse_event("evidence", [e.model_dump() for e in seed_evidence])
            yield sse_event("done", {
                "request_id": context.request_id, "session_id": session_id,
                "suggested_questions": SUGGESTED_QUESTIONS[context.language],
            })
            return

        # Layer 3 – Orchestration: stream workflow loop
        _log("llm_stream_start", provider=llm_client.provider,
             request_id=context.request_id, session_id=session_id,
             history_turns=len(history), intent=intent.intent)
        t0 = time.monotonic()
        answer_parts: list[str] = []
        result = None
        try:
            async for event in stream_fn(
                context.message, context.language, seed_evidence,
                history=history,
                focus=intent.prompt_focus,
                intent_hint=intent.retrieval_hint,
            ):
                if not isinstance(event, StreamEvent):
                    continue
                if event.event == "tool_call":
                    yield sse_event("tool_call", event.data)
                elif event.event == "tool_result":
                    yield sse_event("tool_result", event.data)
                elif event.event == "answer_delta":
                    text = event.data.get("text", "") if isinstance(event.data, dict) else ""
                    if text:
                        answer_parts.append(text)
                        yield sse_event("answer_delta", {"text": text})
                elif event.event == "complete":
                    result = event.data
        except Exception as exc:
            _log("stream_error", provider=llm_client.provider,
                 request_id=context.request_id,
                 elapsed_ms=round((time.monotonic() - t0) * 1000),
                 error_type=exc.__class__.__name__, error=str(exc))

        # Layer 6 – Self-correction for streaming (non-streaming retry if needed)
        if result:
            result = await self._self_correct_result(
                llm_client, result, context, seed_evidence, history,
            )

        elapsed_ms = round((time.monotonic() - t0) * 1000)
        if result:
            session_store.append(session_id, "user", context.message)
            session_store.append(session_id, "assistant", result.answer)
            _log("llm_stream_done", provider=llm_client.provider,
                 request_id=context.request_id, elapsed_ms=elapsed_ms,
                 answer_len=len(result.answer))
            yield sse_event("evidence", [e.model_dump() for e in result.evidence])
            yield sse_event("done", {
                "request_id": context.request_id, "session_id": session_id,
                "suggested_questions": SUGGESTED_QUESTIONS[context.language],
            })
        else:
            answer = "".join(answer_parts).strip()
            if answer:
                session_store.append(session_id, "user", context.message)
                session_store.append(session_id, "assistant", answer)
            _log("stream_no_result", request_id=context.request_id,
                 elapsed_ms=elapsed_ms, partial_answer_len=len(answer) if answer else 0)
            yield sse_event("evidence", [e.model_dump() for e in seed_evidence])
            yield sse_event("done", {
                "request_id": context.request_id, "session_id": session_id,
                "suggested_questions": SUGGESTED_QUESTIONS[context.language],
            })

    # ── Self-correction helpers ─────────────────────────────────────────────

    async def _self_correct(self, llm_client, llm_result, context, seed_evidence, history, t0):
        """Non-streaming self-correction loop (Layer 3 + Layer 6).

        Asks the model to review its own answer.  If the reviewer says IMPROVE,
        retry the full answer call once more (max MAX_SELF_CORRECTION_ATTEMPTS).
        """
        from app.harness.utils import sanitise_answer

        for attempt in range(MAX_SELF_CORRECTION_ATTEMPTS):
            verdict = await self._run_self_check(llm_client, llm_result.answer, context)
            if verdict is None or verdict.strip().upper().startswith("OK"):
                break
            # Extract improvement instruction
            improve_note = verdict.replace("IMPROVE:", "").strip()
            _log("self_correction_triggered", request_id=context.request_id,
                 attempt=attempt + 1, note=improve_note[:120])
            # Retry with improvement note appended to message
            retry_message = f"{context.message}\n\n[Correction note: {improve_note}]"
            try:
                improved = await llm_client.answer(
                    retry_message, context.language, seed_evidence,
                    history=history,
                )
                if improved and improved.answer:
                    llm_result = improved
            except Exception as exc:
                _log("self_correction_error", request_id=context.request_id,
                     attempt=attempt + 1, error=str(exc))
                break
        return llm_result

    async def _self_correct_result(self, llm_client, result, context, seed_evidence, history):
        """Self-correction for the streaming path (re-runs as non-streaming)."""
        return await self._self_correct(llm_client, result, context, seed_evidence, history, None)

    async def _run_self_check(self, llm_client, answer: str, context) -> str | None:
        """Ask the LLM to review the answer quality. Returns 'OK' or 'IMPROVE: ...'."""
        check_msg = self_check_prompt(context.language, answer)
        try:
            check_result = await llm_client.answer(
                check_msg, context.language, [],
            )
            return check_result.answer if check_result else None
        except Exception:
            return None  # skip correction on reviewer failure

    # ── Fallback helper ─────────────────────────────────────────────────────

    def _fallback(self, context, session_id, seed_evidence):
        _log("fallback_response", request_id=context.request_id, reason="llm_result_none")
        return ChatResponse(
            answer=fallback_answer(context.language, [e.title for e in seed_evidence]),
            evidence=seed_evidence,
            suggested_questions=SUGGESTED_QUESTIONS[context.language],
            request_id=context.request_id,
            session_id=session_id,
            source="fallback",
            tools_called=["search_resume_facts"],
        )
