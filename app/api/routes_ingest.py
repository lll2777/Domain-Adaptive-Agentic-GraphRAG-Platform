from __future__ import annotations

from fastapi import APIRouter

from app.config import get_settings
from app.graph.neo4j_client import Neo4jClient
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
    neo4j = Neo4jClient(user=settings.neo4j_user, password=settings.neo4j_password)
    result = ingest_sample_documents(store, qdrant_indexer=qdrant, neo4j_writer=neo4j)
    return {
        "status": "ok",
        "documents": result["documents"],
        "sqlite_written": result["sqlite_written"],
        "chunks": result["chunks"],
        "sqlite_chunk_written": result["sqlite_chunk_written"],
        "qdrant_status": result["qdrant_status"],
        "qdrant_indexed": result["qdrant_indexed"],
        "graph_entities": result["graph_entities"],
        "graph_relations": result["graph_relations"],
        "neo4j_status": result["neo4j_status"],
        "neo4j_entities": result["neo4j_entities"],
        "neo4j_relations": result["neo4j_relations"],
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
