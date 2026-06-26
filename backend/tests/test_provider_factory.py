from __future__ import annotations

from app.harness.chat_completions_client import ChatCompletionsClient
from app.harness.provider_factory import build_llm_client


def test_default_provider_uses_deepseek(monkeypatch):
    monkeypatch.delenv("AI_PROVIDER", raising=False)
    client = build_llm_client()
    assert isinstance(client, ChatCompletionsClient)
    assert client.provider == "deepseek"
    assert client._model() == "deepseek-v4-flash"
    assert client._base_url() == "https://api.deepseek.com"


def test_qwen_provider_uses_openai_compatible_chat_completions(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "qwen")
    client = build_llm_client()
    assert isinstance(client, ChatCompletionsClient)
    assert client.provider == "qwen"
    assert client._model() == "qwen-plus"
    assert client._base_url() == "https://dashscope.aliyuncs.com/compatible-mode/v1"


def test_deepseek_provider_uses_openai_compatible_chat_completions(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "deepseek")
    client = build_llm_client()
    assert isinstance(client, ChatCompletionsClient)
    assert client.provider == "deepseek"
    assert client._model() == "deepseek-v4-flash"
    assert client._base_url() == "https://api.deepseek.com"


def test_qwen_accepts_dashscope_key_alias(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "qwen")
    monkeypatch.delenv("QWEN_API_KEY", raising=False)
    monkeypatch.setenv("DASHSCOPE_API_KEY", "test-key")
    client = build_llm_client()
    assert client.is_configured()
