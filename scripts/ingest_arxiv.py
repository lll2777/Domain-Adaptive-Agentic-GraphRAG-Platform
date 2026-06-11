from __future__ import annotations

import requests

from app.config import get_settings
from app.ingestion.arxiv_loader import ArxivLoader
from app.ingestion.pipeline import ingest_arxiv_records
from app.graph.neo4j_client import Neo4jClient
from app.retrieval.qdrant_retriever import QdrantRetriever
from app.storage.sqlite_store import SQLiteStore


def main() -> None:
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
        records = ArxivLoader().fetch(
            "Retrieval-Augmented Generation",
            categories=["cs.AI", "cs.CL", "cs.IR"],
            max_results=5,
        )
    except requests.RequestException as exc:
        print(f"Failed to fetch arXiv metadata: {exc}")
        return

    result = ingest_arxiv_records(store, records, qdrant_indexer=qdrant, neo4j_writer=neo4j)
    print(
        f"Fetched {result['records']} arXiv metadata records. "
        f"SQLite wrote {result['sqlite_written']} documents and {result['sqlite_chunk_written']} chunks. "
        f"Qdrant status: {result['qdrant_status']}. Neo4j status: {result['neo4j_status']}."
    )


if __name__ == "__main__":
    main()
