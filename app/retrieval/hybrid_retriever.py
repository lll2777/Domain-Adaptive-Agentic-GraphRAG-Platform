from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.core.documents import Chunk
from app.retrieval.bm25_retriever import BM25Retriever, RetrievalResult
from app.retrieval.graph_retriever import GraphRetrievalResult
from app.retrieval.reranker import SimpleReranker


@dataclass
class HybridSearchResult:
    chunks: list[RetrievalResult]
    graph_context: list[dict[str, object]] = field(default_factory=list)
    source_scores: dict[str, float] = field(default_factory=dict)


class HybridRetriever:
    """Merge BM25, Qdrant, and graph retrieval outputs behind one interface."""

    def __init__(
        self,
        bm25: BM25Retriever,
        qdrant: Any | None = None,
        graph: Any | None = None,
        chunk_lookup: dict[str, Chunk] | None = None,
    ) -> None:
        self.bm25 = bm25
        self.qdrant = qdrant
        self.graph = graph
        self.chunk_lookup = chunk_lookup or {}
        self.reranker = SimpleReranker()
        self.last_graph_context: list[dict[str, object]] = []
        self.last_source_scores: dict[str, float] = {}

    def search(self, query: str, top_k: int = 5, domain: str | None = None) -> list[RetrievalResult]:
        bm25_results = self.bm25.search(query, top_k=top_k)
        qdrant_results = self.qdrant.search(query, top_k=top_k, domain=domain) if self.qdrant is not None else []
        graph_results = self.graph.search(query, top_k=top_k) if self.graph is not None else []

        combined: dict[str, RetrievalResult] = {}
        source_scores: dict[str, float] = {"bm25": 0.0, "qdrant": 0.0, "graph": 0.0}
        graph_context: list[dict[str, object]] = []

        for result in bm25_results:
            combined[result.chunk.chunk_id] = RetrievalResult(chunk=result.chunk, score=result.score, source="bm25")
            source_scores["bm25"] = max(source_scores["bm25"], result.score)

        for result in qdrant_results:
            combined[result.chunk.chunk_id] = RetrievalResult(chunk=result.chunk, score=result.score, source="qdrant")
            source_scores["qdrant"] = max(source_scores["qdrant"], result.score)

        for result in graph_results:
            graph_context.append(
                {
                    "entities": result.entities,
                    "relations": result.relations,
                    "evidence_chunk_ids": result.evidence_chunk_ids,
                    "score": result.score,
                }
            )
            source_scores["graph"] = max(source_scores["graph"], result.score)
            for chunk_id in result.evidence_chunk_ids:
                chunk = self.chunk_lookup.get(chunk_id)
                if chunk is None:
                    continue
                existing = combined.get(chunk_id)
                score = result.score if existing is None else max(existing.score, result.score)
                combined[chunk_id] = RetrievalResult(chunk=chunk, score=score, source="graph")

        self.last_graph_context = graph_context
        self.last_source_scores = source_scores

        normalized = self._normalize_scores(list(combined.values()))
        return self.reranker.rerank(normalized)[:top_k]

    def _normalize_scores(self, results: list[RetrievalResult]) -> list[RetrievalResult]:
        if not results:
            return []
        max_score = max(result.score for result in results) or 1.0
        return [RetrievalResult(chunk=result.chunk, score=result.score / max_score, source=result.source) for result in results]
