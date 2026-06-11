from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

import requests

from app.config import Settings


@dataclass
class LLMResponse:
    text: str


class LLMClient:
    """Provider-neutral LLM interface."""

    def generate(self, prompt: str) -> LLMResponse:
        raise NotImplementedError


class MockLLMClient(LLMClient):
    """Default no-key LLM client for local demos."""

    def generate(self, prompt: str) -> LLMResponse:
        first_line = prompt.strip().splitlines()[0] if prompt.strip() else "No prompt provided."
        return LLMResponse(text=f"Mock answer based on retrieved evidence: {first_line}")


class SupportsPost(Protocol):
    def post(self, url: str, headers: dict[str, str], json: dict[str, object], timeout: int) -> Any:
        """Protocol for requests-like sessions used by tests and runtime."""


class OpenAICompatibleLLMClient(LLMClient):
    """OpenAI-compatible chat completions client configured by environment."""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        session: SupportsPost | None = None,
        timeout: int = 30,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.session = session or requests.Session()
        self.timeout = timeout

    def generate(self, prompt: str) -> LLMResponse:
        if not self.base_url:
            raise ValueError("LLM_BASE_URL is required for OpenAI-compatible mode.")
        if not self.api_key:
            raise ValueError("LLM_API_KEY is required for OpenAI-compatible mode.")
        response = self.session.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json={"model": self.model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.1},
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload = response.json()
        choices = payload.get("choices", []) if isinstance(payload, dict) else []
        if not choices:
            return LLMResponse(text="")
        message = choices[0].get("message", {}) if isinstance(choices[0], dict) else {}
        return LLMResponse(text=str(message.get("content", "")))


def build_llm_client(settings: Settings) -> LLMClient:
    """Build the configured LLM client while keeping mock mode the safe default."""

    provider = settings.llm_provider.lower().replace("_", "-")
    if provider in {"openai-compatible", "openai"}:
        return OpenAICompatibleLLMClient(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key,
            model=settings.llm_model,
        )
    return MockLLMClient()
