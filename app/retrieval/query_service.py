from __future__ import annotations

from app.agent.workflow import QueryWorkflow, QueryWorkflowResult
from app.core.chunking import chunk_document
from app.core.documents import Chunk
from app.ingestion.sample_loader import load_sample_papers
from app.retrieval.bm25_retriever import BM25Retriever
from app.storage.sqlite_store import SQLiteStore


def load_query_chunks(store: SQLiteStore | None = None) -> list[Chunk]:
    """Load chunks for query-time retrieval, preferring persisted SQLite data."""

    if store is not None and store.count_chunks() > 0:
        return store.list_chunks()
    documents = load_sample_papers()
    return [chunk for document in documents for chunk in chunk_document(document)]


def build_query_workflow(store: SQLiteStore | None = None) -> QueryWorkflow:
    """Build the current hybrid-style query workflow from available chunks."""

    chunks = load_query_chunks(store)
    retriever = BM25Retriever()
    retriever.index(chunks)
    return QueryWorkflow(retriever=retriever)


def run_query(
    question: str,
    store: SQLiteStore | None = None,
    domain: str = "ai_paper",
    top_k: int = 5,
) -> QueryWorkflowResult:
    """Run a query against persisted chunks with sample fallback."""

    workflow = build_query_workflow(store)
    return workflow.run(question, domain=domain, top_k=top_k)
