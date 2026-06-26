from __future__ import annotations

import json

from app.harness.openai_client import OpenAIResult
from app.harness.pydantic_tools import chat_completion_tool_schemas, validate_tool_arguments
from app.harness.prompts import system_prompt
from app.harness.tools import execute_tool, serialize_tool_result
from app.models import EvidenceCard, Language

DEFAULT_MODEL = "@cf/deepseek-ai/deepseek-r1-distill-qwen-32b"


class WorkersAIClient:
    provider = "workers_ai"

    def __init__(self, ai_binding, model: str | None = None) -> None:
        self._ai = ai_binding
        self._model_name = model or DEFAULT_MODEL

    def is_configured(self) -> bool:
        return self._ai is not None

    async def answer(self, message: str, language: Language, seed_evidence: list[EvidenceCard]) -> OpenAIResult | None:
        if not self.is_configured():
            return None

        messages = [
            {"role": "system", "content": system_prompt(language)},
            {"role": "user", "content": message},
        ]

        first_response = await self._ai.run(
            self._model_name,
            {"messages": messages, "tools": chat_completion_tool_schemas(), "tool_choice": "auto"},
        )

        tool_calls = (first_response.get("tool_calls") or []) if isinstance(first_response, dict) else []

        if not tool_calls:
            text = str(first_response.get("response") or first_response.get("content") or "").strip() if isinstance(first_response, dict) else str(first_response).strip()
            return OpenAIResult(answer=text, evidence=seed_evidence, tools_called=[], provider=self.provider)

        messages.append({"role": "assistant", "tool_calls": tool_calls})
        tools_called: list[str] = []
        evidence: list[EvidenceCard] = []

        for call in tool_calls:
            function = call.get("function") or {}
            name = function.get("name")
            if not name:
                continue
            raw_args = function.get("arguments")
            arguments = validate_tool_arguments(str(name), _parse_arguments(raw_args))
            tools_called.append(name)
            result = execute_tool(name, arguments, language)
            if isinstance(result, list):
                evidence.extend(item for item in result if isinstance(item, EvidenceCard))
            elif isinstance(result, EvidenceCard):
                evidence.append(result)
            messages.append({
                "role": "tool",
                "tool_call_id": call.get("id"),
                "content": json.dumps(serialize_tool_result(result), ensure_ascii=False),
            })

        if not evidence:
            evidence = seed_evidence

        final_response = await self._ai.run(self._model_name, {"messages": messages})
        answer = str(final_response.get("response") or final_response.get("content") or "").strip() if isinstance(final_response, dict) else str(final_response).strip()
        if not answer:
            return None
        return OpenAIResult(answer=answer, evidence=_dedupe_evidence(evidence), tools_called=tools_called, provider=self.provider)


def _parse_arguments(raw_arguments) -> dict:
    if isinstance(raw_arguments, dict):
        return raw_arguments
    if not raw_arguments:
        return {}
    try:
        parsed = json.loads(str(raw_arguments))
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _dedupe_evidence(items: list[EvidenceCard]) -> list[EvidenceCard]:
    seen: set[str] = set()
    deduped: list[EvidenceCard] = []
    for item in items:
        key = item.id or item.title
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped
