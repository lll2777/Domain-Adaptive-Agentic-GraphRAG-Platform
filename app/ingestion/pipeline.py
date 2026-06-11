from __future__ import annotations

from pathlib import Path

from app.core.chunking import chunk_document
from app.core.documents import Chunk, Document
from app.ingestion.sample_loader import load_sample_papers
from app.storage.sqlite_store import SQLiteStore


def build_chunks(documents: list[Document]) -> list[Chunk]:
    """Chunk documents for retrieval and future persistence."""

    return [chunk for document in documents for chunk in chunk_document(document)]


def ingest_sample_documents(store: SQLiteStore, path: Path | None = None) -> dict[str, int]:
    """Load bundled sample data and persist documents to SQLite."""

    documents = load_sample_papers(path)
    written = store.upsert_documents(documents)
    chunks = [chunk for document in documents for chunk in chunk_document(document)]
    chunk_written = store.upsert_chunks(chunks)
    return {
        "documents": len(documents),
        "sqlite_written": written,
        "chunks": len(chunks),
        "sqlite_chunk_written": chunk_written,
    }
