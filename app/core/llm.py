from __future__ import annotations

from dataclasses import dataclass


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
