"""Tests for feedback.py. They use a fake client, so no API key is needed."""

import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from feedback import build_prompt, detect_language, get_feedback  # noqa: E402


class FakeMessages:
    def __init__(self):
        self.last_call = None

    def create(self, **kwargs):
        self.last_call = kwargs
        return SimpleNamespace(content=[SimpleNamespace(text="Bugs: none found.")])


class FakeClient:
    def __init__(self):
        self.messages = FakeMessages()


def test_detect_language():
    assert detect_language("main.py") == "Python"
    assert detect_language("Main.JAVA") == "Java"
    assert detect_language("notes.txt") == "unknown language"


def test_prompt_contains_code_and_level():
    prompt = build_prompt("print('hi')", "Python", "beginner")
    assert "print('hi')" in prompt
    assert "beginner" in prompt


def test_get_feedback_returns_model_text():
    client = FakeClient()
    result = get_feedback("x = 1", client=client)
    assert result == "Bugs: none found."
    # check that the code was actually sent to the model
    sent = client.messages.last_call["messages"][0]["content"]
    assert "x = 1" in sent


def test_empty_code_is_rejected():
    with pytest.raises(ValueError):
        get_feedback("   \n", client=FakeClient())
