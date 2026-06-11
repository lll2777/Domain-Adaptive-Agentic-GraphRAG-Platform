from __future__ import annotations

from pathlib import Path
from typing import Protocol

from app.core.chunking import chunk_document
from app.core.documents import Chunk, Document
from app.graph.graph_builder import build_graph_records
from app.ingestion.sample_loader import load_sample_papers
from app.storage.sqlite_store import SQLiteStore


class ChunkIndexer(Protocol):
    def index_chunks(self, chunks: list[Chunk]) -> dict[str, object]:
        """Index chunks into an external vector store."""


class GraphWriter(Protocol):
    def write_graph(self, entities: list[dict[str, object]], relations: list[dict[str, object]]) -> dict[str, object]:
        """Write graph records to a graph database."""


def build_chunks(documents: list[Document]) -> list[Chunk]:
    """Chunk documents for retrieval and future persistence."""

    return [chunk for document in documents for chunk in chunk_document(document)]


def ingest_sample_documents(
    store: SQLiteStore,
    path: Path | None = None,
    qdrant_indexer: ChunkIndexer | None = None,
    neo4j_writer: GraphWriter | None = None,
) -> dict[str, int | str]:
    """Load bundled sample data and persist documents to SQLite."""

    documents = load_sample_papers(path)
    written = store.upsert_documents(documents)
    chunks = [chunk for document in documents for chunk in chunk_document(document)]
    chunk_written = store.upsert_chunks(chunks)
    qdrant_result = (
        qdrant_indexer.index_chunks(chunks)
        if qdrant_indexer is not None
        else {"status": "skipped", "indexed": 0, "message": "No Qdrant indexer configured."}
    )
    graph_records = build_graph_records(documents)
    entities = graph_records["entities"]
    relations = graph_records["relations"]
    neo4j_result = (
        neo4j_writer.write_graph(entities, relations)
        if neo4j_writer is not None
        else {"status": "skipped", "entities": 0, "relations": 0, "message": "No Neo4j writer configured."}
    )
    return {
        "documents": len(documents),
        "sqlite_written": written,
        "chunks": len(chunks),
        "sqlite_chunk_written": chunk_written,
        "qdrant_status": str(qdrant_result.get("status", "unknown")),
        "qdrant_indexed": int(qdrant_result.get("indexed", 0)),
        "graph_entities": len(entities),
        "graph_relations": len(relations),
        "neo4j_status": str(neo4j_result.get("status", "unknown")),
        "neo4j_entities": int(neo4j_result.get("entities", 0)),
        "neo4j_relations": int(neo4j_result.get("relations", 0)),
    }
