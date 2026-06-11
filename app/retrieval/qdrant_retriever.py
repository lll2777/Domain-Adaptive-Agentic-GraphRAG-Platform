from __future__ import annotations

from app.retrieval.bm25_retriever import RetrievalResult


class QdrantRetriever:
    """Qdrant adapter skeleton; first-stage app falls back gracefully if unavailable."""

    def search(self, query: str, top_k: int = 5, domain: str | None = None) -> list[RetrievalResult]:
        return []
