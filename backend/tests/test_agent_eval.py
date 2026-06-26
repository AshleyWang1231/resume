from __future__ import annotations

import json
import asyncio
from pathlib import Path

import pytest

from app.harness.agent import ResumeAgent
from app.harness.events import stream_chat_response
from app.models import ChatRequest


CASES = json.loads((Path(__file__).parent / "eval_cases.json").read_text())


@pytest.mark.parametrize("case", CASES, ids=[case["id"] for case in CASES])
def test_resume_agent_fallback_eval_cases(case):
    response = asyncio.run(ResumeAgent().answer(ChatRequest(message=case["message"], language=case["language"])))
    evidence_text = json.dumps([item.model_dump() for item in response.evidence], ensure_ascii=False)

    for expected_id in case["expected_project_ids"]:
        assert expected_id in {item.id for item in response.evidence}

    for required in case["must_include"]:
        assert required in response.answer or required in evidence_text


def test_stream_response_contains_answer_and_evidence_events():
    async def collect_stream():
        response = await ResumeAgent().answer(
            ChatRequest(message="Show Lu's Streaming and Tool Calling experience.", language="en")
        )
        return [event async for event in stream_chat_response(response)]

    stream = asyncio.run(collect_stream())
    stream_text = "".join(stream)

    assert "event: metadata" in stream_text
    assert "event: answer_delta" in stream_text
    assert "event: evidence" in stream_text
    assert "event: done" in stream_text
    assert "Agent Runtime Upgrade" in stream_text
