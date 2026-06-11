from __future__ import annotations

from fastapi import APIRouter

from app.config import get_settings
from app.ingestion.pipeline import ingest_sample_documents
from app.retrieval.qdrant_retriever import QdrantRetriever
from app.storage.sqlite_store import SQLiteStore

router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("/sample")
def ingest_sample() -> dict[str, object]:
    """Load bundled sample metadata for the first-stage demo."""

    settings = get_settings()
    store = SQLiteStore(settings.sqlite_path)
    qdrant = QdrantRetriever(host=settings.qdrant_host, port=settings.qdrant_port)
    result = ingest_sample_documents(store, qdrant_indexer=qdrant)
    return {
        "status": "ok",
        "documents": result["documents"],
        "sqlite_written": result["sqlite_written"],
        "chunks": result["chunks"],
        "sqlite_chunk_written": result["sqlite_chunk_written"],
        "qdrant_status": result["qdrant_status"],
        "qdrant_indexed": result["qdrant_indexed"],
        "message": f"Sample records stored in {settings.sqlite_path}.",
    }


@router.post("/arxiv")
def ingest_arxiv(keyword: str = "Retrieval-Augmented Generation", max_results: int = 50) -> dict[str, object]:
    """Return a safe placeholder for arXiv ingest until phase 2 persists data."""

    return {
        "status": "planned",
        "keyword": keyword,
        "max_results": min(max_results, 50),
        "message": "arXiv metadata loader skeleton is available; persistence arrives in phase 2.",
    }
