from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterable

from app.core.documents import Chunk, Document


class SQLiteStore:
    """Small SQLite metadata store prepared for phase 2 ingestion."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def initialize(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS documents (
                    doc_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    source TEXT NOT NULL,
                    text TEXT NOT NULL,
                    metadata TEXT NOT NULL DEFAULT '{}'
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS chunks (
                    chunk_id TEXT PRIMARY KEY,
                    doc_id TEXT NOT NULL,
                    text TEXT NOT NULL,
                    section TEXT,
                    page INTEGER,
                    metadata TEXT NOT NULL DEFAULT '{}'
                )
                """
            )

    def upsert_documents(self, documents: Iterable[Document]) -> int:
        """Insert or update documents in SQLite."""

        rows = [
            (
                document.doc_id,
                document.title,
                document.domain,
                document.source,
                document.text,
                json.dumps(document.metadata, ensure_ascii=False),
            )
            for document in documents
        ]
        if not rows:
            return 0

        self.initialize()
        with sqlite3.connect(self.path) as conn:
            conn.executemany(
                """
                INSERT INTO documents (doc_id, title, domain, source, text, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(doc_id) DO UPDATE SET
                    title = excluded.title,
                    domain = excluded.domain,
                    source = excluded.source,
                    text = excluded.text,
                    metadata = excluded.metadata
                """,
                rows,
            )
            conn.commit()
        return len(rows)

    def count_documents(self) -> int:
        """Return the number of stored documents."""

        self.initialize()
        with sqlite3.connect(self.path) as conn:
            row = conn.execute("SELECT COUNT(*) FROM documents").fetchone()
        return int(row[0] if row else 0)

    def list_documents(self) -> list[Document]:
        """Read all stored documents back into Pydantic models."""

        self.initialize()
        with sqlite3.connect(self.path) as conn:
            rows = conn.execute(
                "SELECT doc_id, title, domain, source, text, metadata FROM documents ORDER BY title"
            ).fetchall()
        documents: list[Document] = []
        for doc_id, title, domain, source, text, metadata_json in rows:
            documents.append(
                Document(
                    doc_id=doc_id,
                    title=title,
                    text=text,
                    source=source,
                    domain=domain,
                    metadata=json.loads(metadata_json or "{}"),
                )
            )
        return documents

    def upsert_chunks(self, chunks: Iterable[Chunk]) -> int:
        """Insert or update chunks in SQLite."""

        rows = [
            (
                chunk.chunk_id,
                chunk.doc_id,
                chunk.text,
                chunk.section,
                chunk.page,
                json.dumps(chunk.metadata, ensure_ascii=False),
            )
            for chunk in chunks
        ]
        if not rows:
            return 0

        self.initialize()
        with sqlite3.connect(self.path) as conn:
            conn.executemany(
                """
                INSERT INTO chunks (chunk_id, doc_id, text, section, page, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(chunk_id) DO UPDATE SET
                    doc_id = excluded.doc_id,
                    text = excluded.text,
                    section = excluded.section,
                    page = excluded.page,
                    metadata = excluded.metadata
                """,
                rows,
            )
            conn.commit()
        return len(rows)

    def count_chunks(self) -> int:
        """Return the number of stored chunks."""

        self.initialize()
        with sqlite3.connect(self.path) as conn:
            row = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()
        return int(row[0] if row else 0)

    def list_chunks(self) -> list[Chunk]:
        """Read all stored chunks back into Pydantic models."""

        self.initialize()
        with sqlite3.connect(self.path) as conn:
            rows = conn.execute(
                "SELECT chunk_id, doc_id, text, section, page, metadata FROM chunks ORDER BY chunk_id"
            ).fetchall()
        chunks: list[Chunk] = []
        for chunk_id, doc_id, text, section, page, metadata_json in rows:
            chunks.append(
                Chunk(
                    chunk_id=chunk_id,
                    doc_id=doc_id,
                    text=text,
                    section=section,
                    page=page,
                    metadata=json.loads(metadata_json or "{}"),
                )
            )
        return chunks
