from __future__ import annotations

from app.retrieval.bm25_retriever import RetrievalResult


class SimpleReranker:
    """First-stage score-based reranker with a future cross-encoder interface."""

    def rerank(self, results: list[RetrievalResult]) -> list[RetrievalResult]:
        return sorted(results, key=lambda result: result.score, reverse=True)
