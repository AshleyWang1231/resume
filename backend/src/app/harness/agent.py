from __future__ import annotations

import time
import uuid
from collections.abc import AsyncIterator

from app.harness.events import sse_event
from app.harness.events import _chunk_text
from app.harness.guard import guard
from app.harness.prompts import fallback_answer
from app.harness.provider_factory import LLMClient, build_llm_client
from app.harness.router import route_intent
from app.harness.stream_types import StreamEvent
from app.harness.tools import search_resume_facts
from app.harness.utils import log as _log
from app.models import AgentContext, ChatRequest, ChatResponse
from app.resume_data import SUGGESTED_QUESTIONS
from app.session import session_store


class ResumeAgent:
    def __init__(self, llm_client: LLMClient | None = None) -> None:
        self.llm_client = llm_client

    async def answer(self, request: ChatRequest, ai_binding=None) -> ChatResponse:
        llm_client = self.llm_client or build_llm_client(ai_binding)
        session_id = request.session_id or str(uuid.uuid4())
        history = session_store.get_history(session_id)

        context = AgentContext(
            request_id=str(uuid.uuid4()),
            message=request.message.strip(),
            language=request.language,
            intent=route_intent(request.message),
            session_id=session_id,
        )

        guard_result = guard(context.message)
        if not guard_result.ok:
            _log("guard_blocked", request_id=context.request_id, reason=guard_result.reason)
            reply = guard_result.reply_zh if request.language == "zh" else guard_result.reply_en
            return ChatResponse(
                answer=reply,
                evidence=[],
                suggested_questions=SUGGESTED_QUESTIONS[context.language],
                request_id=context.request_id,
                session_id=session_id,
                source="guard",
                tools_called=[],
            )
        seed_evidence = search_resume_facts(context.message, context.language)
        _log("retrieval_done", request_id=context.request_id, evidence_count=len(seed_evidence),
             titles=[e.title for e in seed_evidence])

        if not llm_client.is_configured():
            _log("llm_not_configured", provider=llm_client.provider, request_id=context.request_id)
            llm_result = None
        else:
            _log("llm_call_start", provider=llm_client.provider, request_id=context.request_id,
                 session_id=session_id, history_turns=len(history), model_hint=getattr(llm_client, "default_model", ""))
            t0 = time.monotonic()
            try:
                llm_result = await llm_client.answer(
                    context.message,
                    context.language,
                    seed_evidence,
                    history=history,
                )
                elapsed_ms = round((time.monotonic() - t0) * 1000)
                _log("llm_call_done", provider=llm_client.provider, request_id=context.request_id,
                     elapsed_ms=elapsed_ms, has_result=llm_result is not None,
                     tools_called=llm_result.tools_called if llm_result else [])
            except Exception as exc:
                elapsed_ms = round((time.monotonic() - t0) * 1000)
                _log("llm_call_error", provider=llm_client.provider, request_id=context.request_id,
                     elapsed_ms=elapsed_ms, error_type=exc.__class__.__name__, error_message=str(exc))
                llm_result = None

        if llm_result:
            session_store.append(session_id, "user", context.message)
            session_store.append(session_id, "assistant", llm_result.answer)
            return ChatResponse(
                answer=llm_result.answer,
                evidence=llm_result.evidence,
                suggested_questions=SUGGESTED_QUESTIONS[context.language],
                request_id=context.request_id,
                session_id=session_id,
                source=llm_result.provider,
                tools_called=llm_result.tools_called,
            )

        _log("fallback_response", request_id=context.request_id, reason="llm_result_none")
        return ChatResponse(
            answer=fallback_answer(context.language, [item.title for item in seed_evidence]),
            evidence=seed_evidence,
            suggested_questions=SUGGESTED_QUESTIONS[context.language],
            request_id=context.request_id,
            session_id=session_id,
            source="fallback",
            tools_called=["search_resume_facts"],
        )

    async def stream(self, request: ChatRequest, ai_binding=None) -> AsyncIterator[str]:
        llm_client = self.llm_client or build_llm_client(ai_binding)
        session_id = request.session_id or str(uuid.uuid4())
        history = session_store.get_history(session_id)

        context = AgentContext(
            request_id=str(uuid.uuid4()),
            message=request.message.strip(),
            language=request.language,
            intent=route_intent(request.message),
            session_id=session_id,
        )

        guard_result = guard(context.message)
        if not guard_result.ok:
            _log("guard_blocked", request_id=context.request_id, reason=guard_result.reason)
            reply = guard_result.reply_zh if request.language == "zh" else guard_result.reply_en
            yield sse_event("metadata", {
                "request_id": context.request_id,
                "session_id": session_id,
                "source": "guard",
                "tools_called": [],
            })
            for chunk in _chunk_text(reply):
                yield sse_event("answer_delta", {"text": chunk})
            yield sse_event("evidence", [])
            yield sse_event("done", {
                "request_id": context.request_id,
                "session_id": session_id,
                "suggested_questions": SUGGESTED_QUESTIONS[context.language],
            })
            return
        seed_evidence = search_resume_facts(context.message, context.language)
        _log("retrieval_done", request_id=context.request_id, evidence_count=len(seed_evidence),
             titles=[e.title for e in seed_evidence])

        yield sse_event("metadata", {
            "request_id": context.request_id,
            "session_id": session_id,
            "source": llm_client.provider,
            "tools_called": [],
        })

        stream_fn = getattr(llm_client, "stream_answer", None)
        if not callable(stream_fn) or not llm_client.is_configured():
            _log("stream_fallback", request_id=context.request_id, provider=llm_client.provider)
            fallback_text = fallback_answer(context.language, [item.title for item in seed_evidence])
            for chunk in _chunk_text(fallback_text):
                yield sse_event("answer_delta", {"text": chunk})
            yield sse_event("evidence", [item.model_dump() for item in seed_evidence])
            yield sse_event("done", {
                "request_id": context.request_id,
                "session_id": session_id,
                "suggested_questions": SUGGESTED_QUESTIONS[context.language],
            })
            return

        _log("llm_stream_start", provider=llm_client.provider, request_id=context.request_id,
             session_id=session_id, history_turns=len(history))
        t0 = time.monotonic()
        answer_parts: list[str] = []
        result = None
        try:
            async for event in stream_fn(context.message, context.language, seed_evidence, history=history):
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
            elapsed_ms = round((time.monotonic() - t0) * 1000)
            _log("stream_error", provider=llm_client.provider, request_id=context.request_id,
                 elapsed_ms=elapsed_ms, error_type=exc.__class__.__name__, error=str(exc))

        elapsed_ms = round((time.monotonic() - t0) * 1000)
        if result:
            session_store.append(session_id, "user", context.message)
            session_store.append(session_id, "assistant", result.answer)
            _log("llm_stream_done", provider=llm_client.provider, request_id=context.request_id,
                 elapsed_ms=elapsed_ms, answer_len=len(result.answer))
            yield sse_event("evidence", [item.model_dump() for item in result.evidence])
            yield sse_event("done", {"request_id": context.request_id, "session_id": session_id,
                                     "suggested_questions": SUGGESTED_QUESTIONS[context.language]})
        else:
            answer = "".join(answer_parts).strip()
            if answer:
                session_store.append(session_id, "user", context.message)
                session_store.append(session_id, "assistant", answer)
            _log("stream_no_result", request_id=context.request_id, elapsed_ms=elapsed_ms,
                 partial_answer_len=len(answer) if answer else 0)
            yield sse_event("evidence", [item.model_dump() for item in seed_evidence])
            yield sse_event("done", {"request_id": context.request_id, "session_id": session_id,
                                     "suggested_questions": SUGGESTED_QUESTIONS[context.language]})
