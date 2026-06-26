from __future__ import annotations

import json
import uuid

from app.harness.prompts import fallback_answer, system_prompt_with_history
from app.harness.provider_factory import LLMClient, build_llm_client
from app.harness.router import route_intent
from app.harness.tools import search_resume_facts
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
        seed_evidence = search_resume_facts(context.message, context.language)

        if not llm_client.is_configured():
            print(json.dumps({"event": "llm_not_configured", "provider": llm_client.provider, "request_id": context.request_id}))
            llm_result = None
        else:
            print(json.dumps({"event": "llm_call_start", "provider": llm_client.provider, "request_id": context.request_id, "session_id": session_id, "history_turns": len(history)}))
            try:
                llm_result = await llm_client.answer(
                    context.message,
                    context.language,
                    seed_evidence,
                    history=history,
                )
            except Exception as exc:
                print(json.dumps({"event": "llm_call_error", "provider": llm_client.provider, "error_type": exc.__class__.__name__, "error_message": str(exc), "request_id": context.request_id}))
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

        return ChatResponse(
            answer=fallback_answer(context.language, [item.title for item in seed_evidence]),
            evidence=seed_evidence,
            suggested_questions=SUGGESTED_QUESTIONS[context.language],
            request_id=context.request_id,
            session_id=session_id,
            source="fallback",
            tools_called=["search_resume_facts"],
        )
