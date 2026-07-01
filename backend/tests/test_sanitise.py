"""Tests for output sanitisation utility."""
from __future__ import annotations

import pytest

from app.harness.utils import sanitise_answer


@pytest.mark.parametrize("raw, expected", [
    # XML error tags stripped
    ("<error>无法提供相关信息。</error>", "无法提供相关信息。"),
    ("<error> some message </error>", "some message"),
    ("<answer>plain text</answer>", "plain text"),
    # Markdown headers stripped
    ("### Heading\nsome text", "Heading\nsome text"),
    ("## Title\n\nbody", "Title\n\nbody"),
    # Bold/italic stripped
    ("**bold** text", "bold text"),
    ("*italic* word", "italic word"),
    ("__bold__ text", "bold text"),
    # List markers stripped
    ("- item one\n- item two", "item one\nitem two"),
    ("* item\n* other", "item\nother"),
    ("1. first\n2. second", "first\nsecond"),
    # Plain text unchanged
    ("Lu Wang built an agent system.", "Lu Wang built an agent system."),
    # Combined
    (
        "<error>### Not found\n**No data** available</error>",
        "Not found\nNo data available",
    ),
])
def test_sanitise(raw: str, expected: str) -> None:
    assert sanitise_answer(raw) == expected
