from app.core.documents import Chunk
from app.retrieval.bm25_retriever import BM25Retriever


def test_bm25_returns_related_chunk() -> None:
    chunks = [
        Chunk(chunk_id="c1", doc_id="d1", text="GraphRAG builds a graph for multi-hop retrieval."),
        Chunk(chunk_id="c2", doc_id="d2", text="A cooking recipe describes bread and flour."),
    ]
    retriever = BM25Retriever()
    retriever.index(chunks)

    results = retriever.search("graph retrieval", top_k=1)

    assert results
    assert results[0].chunk.chunk_id == "c1"
    assert results[0].score > 0
