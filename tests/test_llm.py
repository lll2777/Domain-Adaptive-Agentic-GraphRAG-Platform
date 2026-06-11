import requests

from app.config import Settings
from app.core.llm import MockLLMClient, OpenAICompatibleLLMClient, build_llm_client


class FakeResponse:
    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict[str, object]:
        return {"choices": [{"message": {"content": "grounded answer"}}]}


class FakeSession:
    def __init__(self) -> None:
        self.payloads: list[dict[str, object]] = []

    def post(self, url: str, headers: dict[str, str], json: dict[str, object], timeout: int) -> FakeResponse:
        self.payloads.append(json)
        return FakeResponse()


def test_build_llm_client_defaults_to_mock() -> None:
    settings = Settings(llm_provider="mock")

    assert isinstance(build_llm_client(settings), MockLLMClient)


def test_openai_compatible_llm_client_posts_chat_completion_payload() -> None:
    session = FakeSession()
    client = OpenAICompatibleLLMClient(
        base_url="https://llm.example/v1",
        api_key="not-real",
        model="demo-model",
        session=session,
    )

    response = client.generate("Use evidence.")

    assert response.text == "grounded answer"
    assert session.payloads[0]["model"] == "demo-model"
    assert session.payloads[0]["messages"][0]["content"] == "Use evidence."


def test_openai_compatible_llm_client_returns_clear_error_without_api_key() -> None:
    client = OpenAICompatibleLLMClient(base_url="https://llm.example/v1", api_key="", model="demo-model")

    try:
        client.generate("prompt")
    except ValueError as exc:
        assert "LLM_API_KEY" in str(exc)
    else:
        raise AssertionError("expected missing key error")
