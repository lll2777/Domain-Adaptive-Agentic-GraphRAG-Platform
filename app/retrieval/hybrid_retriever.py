from __future__ import annotations

from app.retrieval.bm25_retriever import BM25Retriever, RetrievalResult
from app.retrieval.reranker import SimpleReranker


class HybridRetriever:
    """Merge retriever outputs behind one interface."""

    def __init__(self, bm25: BM25Retriever) -> None:
        self.bm25 = bm25
        self.reranker = SimpleReranker()

    def search(self, query: str, top_k: int = 5) -> list[RetrievalResult]:
        results = self.bm25.search(query, top_k=top_k)
        deduped = {result.chunk.chunk_id: result for result in results}
        return self.reranker.rerank(list(deduped.values()))[:top_k]
