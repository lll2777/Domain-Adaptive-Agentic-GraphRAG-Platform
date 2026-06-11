from app.core.documents import Chunk
from app.retrieval.bm25_retriever import RetrievalResult
from app.retrieval.graph_retriever import GraphRetrievalResult
from app.retrieval.hybrid_retriever import HybridRetriever


class FakeBM25:
    def search(self, query: str, top_k: int = 5) -> list[RetrievalResult]:
        return [
            RetrievalResult(
                chunk=Chunk(chunk_id="chunk-1", doc_id="paper-1", text="GraphRAG uses graph retrieval."),
                score=0.2,
                source="bm25",
            )
        ]


class FakeQdrant:
    def search(self, query: str, top_k: int = 5, domain: str | None = None) -> list[RetrievalResult]:
        return [
            RetrievalResult(chunk=Chunk(chunk_id="chunk-2", doc_id="paper-2", text="Qdrant vector retrieval."), score=0.9, source="qdrant")
        ]


class FakeGraph:
    def search(self, query: str, top_k: int = 5) -> list[GraphRetrievalResult]:
        return [
            GraphRetrievalResult(
                evidence_chunk_ids=["chunk-3"],
                entities=[{"entity_id": "e1", "name": "GraphRAG"}],
                relations=[{"relation_type": "PROPOSES"}],
                score=0.8,
            )
        ]


def test_hybrid_retriever_merges_and_dedupes_sources() -> None:
    chunk_lookup = {
        "chunk-1": Chunk(chunk_id="chunk-1", doc_id="paper-1", text="GraphRAG uses graph retrieval."),
        "chunk-2": Chunk(chunk_id="chunk-2", doc_id="paper-2", text="BM25 and vector retrieval."),
        "chunk-3": Chunk(chunk_id="chunk-3", doc_id="paper-3", text="Graph evidence chunk."),
    }
    hybrid = HybridRetriever(bm25=FakeBM25(), qdrant=FakeQdrant(), graph=FakeGraph(), chunk_lookup=chunk_lookup)

    results = hybrid.search("GraphRAG", top_k=3)

    assert [result.chunk.chunk_id for result in results] == ["chunk-2", "chunk-3", "chunk-1"]
    assert hybrid.last_graph_context[0]["evidence_chunk_ids"] == ["chunk-3"]
