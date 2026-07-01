from __future__ import annotations

import json
import os
from collections.abc import AsyncIterator
from typing import Any

import httpx

from app.harness.openai_client import OpenAIResult
from app.harness.pydantic_tools import chat_completion_tool_schemas, validate_tool_arguments
from app.harness.prompts import system_prompt, system_prompt_with_history
from app.harness.stream_types import StreamEvent
from app.harness.tools import execute_tool, serialize_tool_result
from app.harness.utils import dedupe_evidence, log, parse_arguments
from app.models import EvidenceCard, Language


class ChatCompletionsClient:
    def __init__(
        self,
        provider: str,
        api_key_env: str,
        model_env: str,
        default_model: str,
        base_url_env: str,
        default_base_url: str,
        api_key_aliases: tuple[str, ...] = (),
    ) -> None:
        self.provider = provider
        self.api_key_env = api_key_env
        self.model_env = model_env
        self.default_model = default_model
        self.base_url_env = base_url_env
        self.default_base_url = default_base_url.rstrip("/")
        self.api_key_aliases = api_key_aliases

    def is_configured(self) -> bool:
        return bool(self._api_key())

    async def answer(
        self,
        message: str,
        language: Language,
        seed_evidence: list[EvidenceCard],
        history: list[dict[str, str]] | None = None,
    ) -> OpenAIResult | None:
        if not self.is_configured():
            return None

        sys_prompt = system_prompt_with_history(language) if history else system_prompt(language)
        messages: list[dict[str, Any]] = [{"role": "system", "content": sys_prompt}]
        if history:
            messages.extend({"role": h["role"], "content": h["content"]} for h in history[-6:])
        messages.append({"role": "user", "content": message})

        _log("llm_http_start", provider=self.provider, model=self._model(), step="first_pass")
        first_response = await self._post_chat_completions(
            {"model": self._model(), "messages": messages, "tools": chat_completion_tool_schemas(), "tool_choice": "auto"}
        )
        assistant_message = _extract_assistant_message(first_response)
        tool_calls = assistant_message.get("tool_calls") or []

        if not tool_calls:
            text = str(assistant_message.get("content") or "").strip()
            _log("llm_http_done", provider=self.provider, step="first_pass", has_tools=False, answer_len=len(text))
            return OpenAIResult(answer=text, evidence=seed_evidence, tools_called=[], provider=self.provider)

        _log("llm_http_done", provider=self.provider, step="first_pass", has_tools=True, tool_count=len(tool_calls))
        messages.append(assistant_message)
        tools_called: list[str] = []
        evidence: list[EvidenceCard] = []

        for call in tool_calls:
            function = call.get("function") or {}
            name = function.get("name")
            if not name:
                continue
            arguments = validate_tool_arguments(str(name), parse_arguments(function.get("arguments")))
            tools_called.append(name)
            _log("tool_execute", provider=self.provider, tool=name)
            result = execute_tool(name, arguments, language)
            if isinstance(result, list):
                evidence.extend(item for item in result if isinstance(item, EvidenceCard))
            elif isinstance(result, EvidenceCard):
                evidence.append(result)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.get("id"),
                    "content": json.dumps(serialize_tool_result(result), ensure_ascii=False),
                }
            )

        if not evidence:
            evidence = seed_evidence

        _log("llm_http_start", provider=self.provider, model=self._model(), step="final_pass")
        final_response = await self._post_chat_completions({"model": self._model(), "messages": messages})
        final_message = _extract_assistant_message(final_response)
        answer = str(final_message.get("content") or "").strip()
        _log("llm_http_done", provider=self.provider, step="final_pass", answer_len=len(answer))

        if not answer:
            return None
        return OpenAIResult(answer=answer, evidence=dedupe_evidence(evidence), tools_called=tools_called, provider=self.provider)

    async def stream_answer(
        self,
        message: str,
        language: Language,
        seed_evidence: list[EvidenceCard],
        history: list[dict[str, str]] | None = None,
    ) -> AsyncIterator[StreamEvent]:
        if not self.is_configured():
            return

        messages = self._build_messages(message, language, history)
        url = f"{self._base_url()}/chat/completions"
        headers = {
            "authorization": f"Bearer {self._api_key()}",
            "content-type": "application/json",
        }
        payload = {
            "model": self._model(),
            "messages": messages,
            "tools": chat_completion_tool_schemas(),
            "tool_choice": "auto",
        }

        _log("llm_stream_start", provider=self.provider, model=self._model(), step="first_pass")
        content_parts: list[str] = []
        tool_calls = await self._stream_first_pass(url, payload, headers, content_parts)
        for delta in content_parts:
            yield StreamEvent("answer_delta", {"text": delta})

        if not tool_calls:
            answer = "".join(content_parts).strip()
            if not answer:
                return
            _log("llm_stream_done", provider=self.provider, step="first_pass_no_tools", answer_len=len(answer))
            yield StreamEvent(
                "complete",
                OpenAIResult(answer=answer, evidence=seed_evidence, tools_called=[], provider=self.provider),
            )
            return

        _log("llm_stream_done", provider=self.provider, step="first_pass", tool_count=len(tool_calls))
        tools_called: list[str] = []
        evidence: list[EvidenceCard] = []
        assistant_tool_calls = []
        for idx in sorted(tool_calls):
            call = tool_calls[idx]
            assistant_tool_calls.append(
                {
                    "id": call["id"],
                    "type": "function",
                    "function": {"name": call["name"], "arguments": call["arguments"]},
                }
            )

        messages.append({"role": "assistant", "content": None, "tool_calls": assistant_tool_calls})

        for call in assistant_tool_calls:
            function = call["function"]
            name = function["name"]
            arguments = validate_tool_arguments(name, _parse_arguments(function["arguments"]))
            tools_called.append(name)
            _log("tool_execute", provider=self.provider, tool=name)
            yield StreamEvent("tool_call", {"name": name})
            result = execute_tool(name, arguments, language)
            if isinstance(result, list):
                evidence.extend(item for item in result if isinstance(item, EvidenceCard))
            elif isinstance(result, EvidenceCard):
                evidence.append(result)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call["id"],
                    "content": json.dumps(serialize_tool_result(result), ensure_ascii=False),
                }
            )

        if tools_called:
            yield StreamEvent("tool_result", {"count": len(evidence or seed_evidence)})

        if not evidence:
            evidence = seed_evidence

        _log("llm_stream_start", provider=self.provider, model=self._model(), step="final_pass")
        content_parts = []
        async with httpx.AsyncClient(timeout=30) as client:
            async with client.stream(
                "POST",
                f"{self._base_url()}/chat/completions",
                headers={"authorization": f"Bearer {self._api_key()}", "content-type": "application/json"},
                content=json.dumps({"model": self._model(), "messages": messages, "stream": True}).encode(),
            ) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if not line.startswith("data: "):
                        continue
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data)
                    except json.JSONDecodeError:
                        continue
                    choices = chunk.get("choices") or []
                    if not choices:
                        continue
                    delta = choices[0].get("delta") or {}
                    text = delta.get("content")
                    if not text:
                        continue
                    content_parts.append(text)
                    yield StreamEvent("answer_delta", {"text": text})

        answer = "".join(content_parts).strip()
        if not answer:
            return
        _log("llm_stream_done", provider=self.provider, step="final_pass", answer_len=len(answer))
        yield StreamEvent(
            "complete",
            OpenAIResult(
                answer=answer,
                evidence=_dedupe_evidence(evidence),
                tools_called=tools_called,
                provider=self.provider,
            ),
        )

    def _build_messages(
        self,
        message: str,
        language: Language,
        history: list[dict[str, str]] | None,
    ) -> list[dict[str, Any]]:
        sys_prompt = system_prompt_with_history(language) if history else system_prompt(language)
        messages: list[dict[str, Any]] = [{"role": "system", "content": sys_prompt}]
        if history:
            messages.extend({"role": h["role"], "content": h["content"]} for h in history[-6:])
        messages.append({"role": "user", "content": message})
        return messages

    async def _post_chat_completions(self, payload: dict[str, Any]) -> dict[str, Any]:
        url = f"{self._base_url()}/chat/completions"
        headers = {
            "authorization": f"Bearer {self._api_key()}",
            "content-type": "application/json",
        }
        async with httpx.AsyncClient(timeout=30) as client:
            try:
                resp = await client.post(url, headers=headers, content=json.dumps(payload).encode())
                resp.raise_for_status()
                return resp.json()
            except httpx.HTTPStatusError as exc:
                detail = exc.response.text[:240]
                raise RuntimeError(f"{self.provider} request failed: {exc.response.status_code} {detail}") from exc

    async def _stream_first_pass(
        self,
        url: str,
        payload: dict[str, Any],
        headers: dict[str, str],
        content_parts: list[str],
    ) -> dict[int, dict[str, str]]:
        tool_calls: dict[int, dict[str, str]] = {}
        payload_with_stream = {**payload, "stream": True}
        async with httpx.AsyncClient(timeout=30) as client:
            async with client.stream(
                "POST",
                url,
                headers=headers,
                content=json.dumps(payload_with_stream).encode(),
            ) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if not line.startswith("data: "):
                        continue
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data)
                    except json.JSONDecodeError:
                        continue
                    choices = chunk.get("choices") or []
                    if not choices:
                        continue
                    delta = choices[0].get("delta") or {}
                    text = delta.get("content")
                    if text:
                        content_parts.append(text)
                    for tool_delta in delta.get("tool_calls") or []:
                        idx = tool_delta.get("index", 0)
                        if idx not in tool_calls:
                            tool_calls[idx] = {"id": "", "name": "", "arguments": ""}
                        if tool_delta.get("id"):
                            tool_calls[idx]["id"] = tool_delta["id"]
                        function = tool_delta.get("function") or {}
                        if function.get("name"):
                            tool_calls[idx]["name"] = function["name"]
                        if function.get("arguments"):
                            tool_calls[idx]["arguments"] += function["arguments"]
        return {idx: call for idx, call in tool_calls.items() if call["id"] and call["name"]}

    def _api_key(self) -> str | None:
        for name in (self.api_key_env, *self.api_key_aliases):
            value = os.getenv(name)
            if value:
                return value
        return None

    def _model(self) -> str:
        return os.getenv(self.model_env) or self.default_model

    def _base_url(self) -> str:
        return (os.getenv(self.base_url_env) or self.default_base_url).rstrip("/")


def _log(event: str, **kwargs: Any) -> None:
    log(event, **kwargs)


def _extract_assistant_message(response: dict[str, Any]) -> dict[str, Any]:
    choices = response.get("choices") or []
    if not choices:
        return {}
    message = choices[0].get("message") or {}
    return message if isinstance(message, dict) else {}
