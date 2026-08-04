from types import SimpleNamespace

import pytest

from bug_triage_assistant import triage


def test_missing_model_content_raises_user_facing_value_error(monkeypatch):
    response = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=None))]
    )
    client = SimpleNamespace(
        chat=SimpleNamespace(completions=SimpleNamespace(create=lambda **kwargs: response))
    )
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(triage, "OpenAI", lambda api_key: client)

    with pytest.raises(ValueError, match="The model returned invalid JSON"):
        triage.triage_bug_report("App crashes on login")
