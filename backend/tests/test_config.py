from __future__ import annotations

import os

from app.config import _load_env_file


def test_load_env_file_supports_quotes_and_export(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "# comment",
                "export AI_PROVIDER=qwen",
                'QWEN_API_KEY="test-key"',
                "QWEN_MODEL='qwen-plus'",
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.delenv("AI_PROVIDER", raising=False)
    monkeypatch.delenv("QWEN_API_KEY", raising=False)
    monkeypatch.delenv("QWEN_MODEL", raising=False)
    _load_env_file(env_file, override=False)

    assert os.environ["AI_PROVIDER"] == "qwen"
    assert os.environ["QWEN_API_KEY"] == "test-key"
    assert os.environ["QWEN_MODEL"] == "qwen-plus"


def test_load_env_file_does_not_override_existing_value(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("AI_PROVIDER=deepseek", encoding="utf-8")

    monkeypatch.setenv("AI_PROVIDER", "openai")
    _load_env_file(env_file, override=False)

    assert os.environ["AI_PROVIDER"] == "openai"
