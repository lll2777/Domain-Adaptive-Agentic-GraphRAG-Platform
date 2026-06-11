from __future__ import annotations

from app.config import get_settings
from app.agent.workflow import QueryWorkflow, QueryWorkflowResult
from app.core.chunking import chunk_document
from app.core.documents import Chunk
from app.retrieval.graph_retriever import GraphRetriever
from app.ingestion.sample_loader import load_sample_papers
from app.retrieval.bm25_retriever import BM25Retriever
from app.retrieval.hybrid_retriever import HybridRetriever
from app.retrieval.qdrant_retriever import QdrantRetriever
from app.storage.sqlite_store import SQLiteStore


def load_query_chunks(store: SQLiteStore | None = None) -> list[Chunk]:
    """Load chunks for query-time retrieval, preferring persisted SQLite data."""

    if store is not None and store.count_chunks() > 0:
        return store.list_chunks()
    documents = load_sample_papers()
    return [chunk for document in documents for chunk in chunk_document(document)]


def build_hybrid_retriever(store: SQLiteStore | None = None) -> HybridRetriever:
    """Build a hybrid retriever from persisted chunks and live adapters."""

    chunks = load_query_chunks(store)
    settings = get_settings()
    bm25 = BM25Retriever()
    bm25.index(chunks)
    chunk_lookup = {chunk.chunk_id: chunk for chunk in chunks}
    qdrant = QdrantRetriever(host=settings.qdrant_host, port=settings.qdrant_port, timeout=2)
    graph = GraphRetriever(user=settings.neo4j_user, password=settings.neo4j_password, timeout=2)
    return HybridRetriever(bm25=bm25, qdrant=qdrant, graph=graph, chunk_lookup=chunk_lookup)


def run_query(
    question: str,
    store: SQLiteStore | None = None,
    domain: str = "ai_paper",
    top_k: int = 5,
) -> QueryWorkflowResult:
    """Run a query against persisted chunks with sample fallback."""

    hybrid = build_hybrid_retriever(store)
    workflow = QueryWorkflow(retriever=hybrid)
    result = workflow.run(question, domain=domain, top_k=top_k)
    result.graph_context = hybrid.last_graph_context
    result.scores.update(
        {
            "bm25_score": hybrid.last_source_scores.get("bm25", 0.0),
            "qdrant_score": hybrid.last_source_scores.get("qdrant", 0.0),
            "graph_score": hybrid.last_source_scores.get("graph", 0.0),
        }
    )
    return result
