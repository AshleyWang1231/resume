# Layer 2 — Tool System (schema generation)
from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class SearchResumeFactsArgs(BaseModel):
    query: str


class GetProjectDetailArgs(BaseModel):
    project_id: str


class ListCapabilitiesArgs(BaseModel):
    pass


_FALLBACK_SCHEMAS: dict[str, dict[str, Any]] = {
    "search_resume_facts": {
        "description": "Search Lu Wang's structured resume facts by query.",
        "model": SearchResumeFactsArgs,
    },
    "get_project_detail": {
        "description": "Get one structured resume project by id.",
        "model": GetProjectDetailArgs,
    },
    "list_capabilities": {
        "description": "List Lu Wang's skill groups and which projects support each skill.",
        "model": ListCapabilitiesArgs,
    },
}


def search_resume_facts(query: str) -> list[dict[str, Any]]:
    """Search Lu Wang's structured resume facts by query."""
    raise RuntimeError("Tool schema function should not be executed directly")


def get_project_detail(project_id: str) -> dict[str, Any] | None:
    """Get one structured resume project by id."""
    raise RuntimeError("Tool schema function should not be executed directly")


def list_capabilities() -> dict[str, list[str]]:
    """List Lu Wang's skill groups and which projects support each skill."""
    raise RuntimeError("Tool schema function should not be executed directly")


def pydantic_tool_registry() -> dict[str, Any]:
    try:
        from pydantic_ai import Tool
    except ModuleNotFoundError:
        return {}

    return {
        "search_resume_facts": Tool(search_resume_facts, name="search_resume_facts", strict=False),
        "get_project_detail": Tool(get_project_detail, name="get_project_detail", strict=False),
        "list_capabilities": Tool(list_capabilities, name="list_capabilities", strict=False),
    }


def chat_completion_tool_schemas() -> list[dict[str, Any]]:
    registry = pydantic_tool_registry()
    if registry:
        return [
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": tool.function_schema.description,
                    "parameters": tool.function_schema.json_schema,
                },
            }
            for name, tool in registry.items()
        ]
    return [
        {
            "type": "function",
            "function": {
                "name": name,
                "description": item["description"],
                "parameters": item["model"].model_json_schema(),
            },
        }
        for name, item in _FALLBACK_SCHEMAS.items()
    ]


def responses_tool_schemas() -> list[dict[str, Any]]:
    registry = pydantic_tool_registry()
    if registry:
        return [
            {
                "type": "function",
                "name": name,
                "description": tool.function_schema.description,
                "parameters": tool.function_schema.json_schema,
            }
            for name, tool in registry.items()
        ]
    return [
        {
            "type": "function",
            "name": name,
            "description": item["description"],
            "parameters": item["model"].model_json_schema(),
        }
        for name, item in _FALLBACK_SCHEMAS.items()
    ]


def validate_tool_arguments(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    tool = pydantic_tool_registry().get(name)
    if tool:
        validated = tool.function_schema.validator.validate_python(arguments)
        return dict(validated)
    fallback = _FALLBACK_SCHEMAS.get(name)
    if not fallback:
        raise ValueError(f"Unsupported tool: {name}")
    return fallback["model"].model_validate(arguments).model_dump(exclude_none=True)
