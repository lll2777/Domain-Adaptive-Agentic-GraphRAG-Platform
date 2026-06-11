from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field
import requests

from app.config import get_settings
from app.graph.neo4j_client import Neo4jClient
from app.ingestion.arxiv_loader import ArxivLoader
from app.ingestion.pipeline import ingest_arxiv_records, ingest_sample_documents
from app.retrieval.qdrant_retriever import QdrantRetriever
from app.storage.sqlite_store import SQLiteStore

router = APIRouter(prefix="/ingest", tags=["ingest"])


class ArxivIngestRequest(BaseModel):
    keyword: str = "Retrieval-Augmented Generation"
    categories: list[str] = Field(default_factory=lambda: ["cs.AI", "cs.CL", "cs.IR"])
    max_results: int = 50


@router.post("/sample")
def ingest_sample() -> dict[str, object]:
    """Load bundled sample metadata for the first-stage demo."""

    settings = get_settings()
    store = SQLiteStore(settings.sqlite_path)
    qdrant = QdrantRetriever(
        host=settings.qdrant_host,
        port=settings.qdrant_port,
        embedding_provider=settings.embedding_provider,
        embedding_model_name=settings.embedding_model,
    )
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
def ingest_arxiv(request: ArxivIngestRequest) -> dict[str, object]:
    """Fetch arXiv metadata and persist it through the same ingestion pipeline."""

    settings = get_settings()
    store = SQLiteStore(settings.sqlite_path)
    qdrant = QdrantRetriever(
        host=settings.qdrant_host,
        port=settings.qdrant_port,
        embedding_provider=settings.embedding_provider,
        embedding_model_name=settings.embedding_model,
    )
    neo4j = Neo4jClient(user=settings.neo4j_user, password=settings.neo4j_password)
    try:
        records = ArxivLoader().fetch(request.keyword, categories=request.categories, max_results=request.max_results)
    except requests.RequestException as exc:
        return {
            "status": "error",
            "keyword": request.keyword,
            "categories": request.categories,
            "max_results": min(request.max_results, 50),
            "records": 0,
            "documents": 0,
            "sqlite_written": 0,
            "chunks": 0,
            "sqlite_chunk_written": 0,
            "qdrant_status": "skipped",
            "qdrant_indexed": 0,
            "graph_entities": 0,
            "graph_relations": 0,
            "neo4j_status": "skipped",
            "neo4j_entities": 0,
            "neo4j_relations": 0,
            "message": f"Failed to fetch arXiv metadata: {exc}",
        }
    result = ingest_arxiv_records(store, records, qdrant_indexer=qdrant, neo4j_writer=neo4j)
    return {
        "status": "ok",
        "keyword": request.keyword,
        "categories": request.categories,
        "max_results": min(request.max_results, 50),
        "records": result["records"],
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
        "message": f"Fetched and stored arXiv metadata in {settings.sqlite_path}.",
    }
