from __future__ import annotations

import os
from pathlib import Path


ENV_NAMES = (
    "AI_PROVIDER",
    "OPENAI_API_KEY",
    "OPENAI_MODEL",
    "QWEN_API_KEY",
    "DASHSCOPE_API_KEY",
    "QWEN_MODEL",
    "QWEN_BASE_URL",
    "DEEPSEEK_API_KEY",
    "DEEPSEEK_MODEL",
    "DEEPSEEK_BASE_URL",
)


def load_local_env(override: bool = False) -> None:
    for path in _candidate_env_paths():
        if path.exists():
            _load_env_file(path, override=override)


def sync_worker_env(env) -> None:
    for name in ENV_NAMES:
        value = getattr(env, name, None)
        if value and not os.getenv(name):
            os.environ[name] = str(value)


def _candidate_env_paths() -> list[Path]:
    backend_dir = Path(__file__).resolve().parents[2]
    paths = [backend_dir / ".env", Path.cwd() / ".env"]
    unique_paths: list[Path] = []
    for path in paths:
        if path not in unique_paths:
            unique_paths.append(path)
    return unique_paths


def _load_env_file(path: Path, override: bool) -> None:
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        name, value = line.split("=", 1)
        name = name.strip()
        if not name or (not override and name in os.environ):
            continue
        os.environ[name] = _strip_quotes(value.strip())


def _strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value
