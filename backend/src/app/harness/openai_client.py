from __future__ import annotations

import json
import os
from typing import Any

import httpx

from app.harness.pydantic_tools import responses_tool_schemas, validate_tool_arguments
from app.harness.prompts import system_prompt
from app.harness.tools import execute_tool, serialize_tool_result
from app.models import EvidenceCard, Language


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
DEFAULT_MODEL = "gpt-4.1-mini"


class OpenAIResult:
    def __init__(
        self,
        answer: str,
        evidence: list[EvidenceCard],
        tools_called: list[str],
        provider: str = "openai",
    ) -> None:
        self.answer = answer
        self.evidence = evidence
        self.tools_called = tools_called
        self.provider = provider


class OpenAIResponsesClient:
    provider = "openai"

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self.api_key = api_key
        self.model = model

    def is_configured(self) -> bool:
        return bool(self._api_key())

    async def answer(self, message: str, language: Language, seed_evidence: list[EvidenceCard]) -> OpenAIResult | None:
        if not self.is_configured():
            return None

        first_payload = {
            "model": self._model(),
            "input": [
                {"role": "system", "content": system_prompt(language)},
                {"role": "user", "content": message},
            ],
            "tools": responses_tool_schemas(),
            "tool_choice": "auto",
        }
        first_response = await self._post_json(first_payload)
        tool_calls = _extract_tool_calls(first_response)
        if not tool_calls:
            text = _extract_output_text(first_response)
            return OpenAIResult(answer=text, evidence=seed_evidence, tools_called=[])

        tool_outputs: list[dict[str, Any]] = []
        tools_called: list[str] = []
        evidence: list[EvidenceCard] = []

        for call in tool_calls:
            name = call["name"]
            arguments = call["arguments"]
            tools_called.append(name)
            result = execute_tool(name, arguments, language)
            if isinstance(result, list):
                evidence.extend(item for item in result if isinstance(item, EvidenceCard))
            elif isinstance(result, EvidenceCard):
                evidence.append(result)
            tool_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": call["call_id"],
                    "output": json.dumps(serialize_tool_result(result), ensure_ascii=False),
                }
            )

        if not evidence:
            evidence = seed_evidence

        final_payload: dict[str, Any] = {"model": self._model(), "input": tool_outputs}
        if first_response.get("id"):
            final_payload["previous_response_id"] = first_response["id"]
        else:
            final_payload["input"] = [
                {"role": "system", "content": system_prompt(language)},
                {"role": "user", "content": message},
                *tool_outputs,
            ]
        final_response = await self._post_json(final_payload)
        answer = _extract_output_text(final_response)
        if not answer:
            return None
        return OpenAIResult(answer=answer, evidence=_dedupe_evidence(evidence), tools_called=tools_called)

    async def _post_json(self, payload: dict[str, Any]) -> dict[str, Any]:
        headers = {
            "authorization": f"Bearer {self._api_key()}",
            "content-type": "application/json",
        }
        async with httpx.AsyncClient(timeout=20) as client:
            try:
                resp = await client.post(OPENAI_RESPONSES_URL, headers=headers, content=json.dumps(payload).encode())
                resp.raise_for_status()
                return resp.json()
            except httpx.HTTPStatusError as exc:
                detail = exc.response.text[:240]
                raise RuntimeError(f"OpenAI request failed: {exc.response.status_code} {detail}") from exc

    def _api_key(self) -> str | None:
        return self.api_key or os.getenv("OPENAI_API_KEY")

    def _model(self) -> str:
        return self.model or os.getenv("OPENAI_MODEL") or DEFAULT_MODEL


def _extract_tool_calls(response: dict[str, Any]) -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []
    for item in response.get("output", []):
        if item.get("type") != "function_call":
            continue
        raw_arguments = item.get("arguments") or "{}"
        try:
            arguments = json.loads(raw_arguments)
        except json.JSONDecodeError:
            arguments = {}
        name = item.get("name")
        if name:
            arguments = validate_tool_arguments(str(name), arguments)
        calls.append(
            {
                "call_id": item.get("call_id"),
                "name": name,
                "arguments": arguments,
            }
        )
    return [call for call in calls if call["call_id"] and call["name"]]


def _extract_output_text(response: dict[str, Any]) -> str:
    if response.get("output_text"):
        return str(response["output_text"])
    chunks: list[str] = []
    for item in response.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"} and content.get("text"):
                chunks.append(str(content["text"]))
    return "".join(chunks).strip()


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
