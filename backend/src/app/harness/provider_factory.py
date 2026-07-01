# Infrastructure — multi-provider LLM factory
from __future__ import annotations

import os
from typing import Protocol

from app.harness.chat_completions_client import ChatCompletionsClient
from app.harness.openai_client import OpenAIResponsesClient, OpenAIResult
from app.models import EvidenceCard, Language


class LLMClient(Protocol):
    provider: str

    def is_configured(self) -> bool: ...

    async def answer(self, message: str, language: Language, seed_evidence: list[EvidenceCard]) -> OpenAIResult | None: ...


def build_llm_client(ai_binding=None) -> LLMClient:
    provider = os.getenv("AI_PROVIDER", "workers_ai").lower()
    if provider == "workers_ai":
        from app.harness.workers_ai_client import WorkersAIClient
        return WorkersAIClient(ai_binding)
    if provider == "qwen":
        return ChatCompletionsClient(
            provider="qwen",
            api_key_env="QWEN_API_KEY",
            api_key_aliases=("DASHSCOPE_API_KEY",),
            model_env="QWEN_MODEL",
            default_model="qwen-turbo",
            base_url_env="QWEN_BASE_URL",
            default_base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
    if provider == "deepseek":
        return ChatCompletionsClient(
            provider="deepseek",
            api_key_env="DEEPSEEK_API_KEY",
            model_env="DEEPSEEK_MODEL",
            default_model="deepseek-v4-flash",
            base_url_env="DEEPSEEK_BASE_URL",
            default_base_url="https://api.deepseek.com",
        )
    return OpenAIResponsesClient()
