from __future__ import annotations

import sqlite3
from pathlib import Path


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
                    source TEXT NOT NULL
                )
                """
            )
