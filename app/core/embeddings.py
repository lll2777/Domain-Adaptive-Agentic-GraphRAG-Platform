from __future__ import annotations

import hashlib
import math
from typing import Any


class HashingEmbeddingModel:
    """Small deterministic embedding fallback that needs no model download."""

    def __init__(self, dimensions: int = 128) -> None:
        self.dimensions = dimensions

    def embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        for token in text.lower().split():
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            vector[index] += 1.0
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]


class SentenceTransformerEmbeddingModel:
    """Optional sentence-transformers adapter with no hard dependency at import time."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", model: Any | None = None) -> None:
        if model is None:
            from sentence_transformers import SentenceTransformer

            model = SentenceTransformer(model_name)
        self.model = model

    def embed(self, text: str) -> list[float]:
        values = self.model.encode(text)
        vector = [float(value) for value in values]
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]


def build_embedding_model(
    provider: str = "hashing",
    dimensions: int = 128,
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
) -> HashingEmbeddingModel | SentenceTransformerEmbeddingModel:
    """Build an embedding model, falling back to hashing when optional models are unavailable."""

    normalized = provider.lower().replace("_", "-")
    if normalized in {"sentence-transformers", "sentence-transformer", "st"}:
        try:
            return SentenceTransformerEmbeddingModel(model_name=model_name)
        except (ImportError, OSError):
            return HashingEmbeddingModel(dimensions=dimensions)
    return HashingEmbeddingModel(dimensions=dimensions)
