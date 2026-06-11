from pathlib import Path

from app.core.documents import Chunk
from app.storage.sqlite_store import SQLiteStore


def test_sqlite_store_persists_chunks(tmp_path: Path) -> None:
    store = SQLiteStore(tmp_path / "app.db")
    store.initialize()

    chunks = [
        Chunk(
            chunk_id="paper-1-0",
            doc_id="paper-1",
            text="Retrieval-Augmented Generation grounds answers.",
            metadata={"doc_id": "paper-1"},
        ),
        Chunk(
            chunk_id="paper-1-1",
            doc_id="paper-1",
            text="GraphRAG links entities and relations.",
            metadata={"doc_id": "paper-1"},
        ),
    ]

    written = store.upsert_chunks(chunks)

    assert written == 2
    assert store.count_chunks() == 2


def test_sqlite_store_returns_chunks(tmp_path: Path) -> None:
    store = SQLiteStore(tmp_path / "app.db")
    store.initialize()
    store.upsert_chunks(
        [
            Chunk(
                chunk_id="paper-1-0",
                doc_id="paper-1",
                text="Retrieval-Augmented Generation grounds answers.",
                metadata={"doc_id": "paper-1"},
            )
        ]
    )

    chunks = store.list_chunks()

    assert len(chunks) == 1
    assert chunks[0].chunk_id == "paper-1-0"
    assert chunks[0].doc_id == "paper-1"
