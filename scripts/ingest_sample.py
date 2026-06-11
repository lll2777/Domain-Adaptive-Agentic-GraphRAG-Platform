from __future__ import annotations

from app.config import get_settings
from app.graph.neo4j_client import Neo4jClient
from app.ingestion.pipeline import ingest_sample_documents
from app.retrieval.qdrant_retriever import QdrantRetriever
from app.storage.sqlite_store import SQLiteStore


def main() -> None:
    settings = get_settings()
    store = SQLiteStore(settings.sqlite_path)
    qdrant = QdrantRetriever(host=settings.qdrant_host, port=settings.qdrant_port)
    neo4j = Neo4jClient(user=settings.neo4j_user, password=settings.neo4j_password)
    result = ingest_sample_documents(store, qdrant_indexer=qdrant, neo4j_writer=neo4j)
    print(
        f"Loaded {result['documents']} sample documents and {result['chunks']} chunks; "
        f"wrote {result['sqlite_written']} documents and {result['sqlite_chunk_written']} chunks to {settings.sqlite_path}. "
        f"Qdrant status: {result['qdrant_status']} ({result['qdrant_indexed']} chunks indexed). "
        f"Neo4j status: {result['neo4j_status']} ({result['neo4j_entities']} entities, {result['neo4j_relations']} relations)."
    )


if __name__ == "__main__":
    main()
