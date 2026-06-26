from __future__ import annotations

import pytest
from pydantic_core import ValidationError

from app.harness.pydantic_tools import chat_completion_tool_schemas, responses_tool_schemas, validate_tool_arguments


def test_pydantic_ai_generates_chat_completion_tool_schemas():
    schemas = chat_completion_tool_schemas()
    names = {schema["function"]["name"] for schema in schemas}

    assert names == {"search_resume_facts", "get_project_detail", "list_capabilities"}
    search_schema = next(schema for schema in schemas if schema["function"]["name"] == "search_resume_facts")
    assert search_schema["function"]["parameters"]["required"] == ["query"]


def test_pydantic_ai_generates_responses_tool_schemas():
    schemas = responses_tool_schemas()
    names = {schema["name"] for schema in schemas}

    assert names == {"search_resume_facts", "get_project_detail", "list_capabilities"}
    detail_schema = next(schema for schema in schemas if schema["name"] == "get_project_detail")
    assert detail_schema["parameters"]["required"] == ["project_id"]


def test_tool_arguments_are_validated_by_pydantic_ai_schema():
    assert validate_tool_arguments("search_resume_facts", {"query": "Streaming"}) == {"query": "Streaming"}

    with pytest.raises(ValidationError):
        validate_tool_arguments("search_resume_facts", {"project_id": "agent-runtime"})
