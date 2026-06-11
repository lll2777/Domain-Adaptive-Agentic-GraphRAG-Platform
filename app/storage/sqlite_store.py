from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterable

from app.core.documents import Document


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
