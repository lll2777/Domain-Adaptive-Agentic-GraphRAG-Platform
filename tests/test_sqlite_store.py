from pathlib import Path

from app.core.documents import Document
from app.storage.sqlite_store import SQLiteStore


def test_sqlite_store_persists_documents(tmp_path: Path) -> None:
    store = SQLiteStore(tmp_path / "app.db")
    store.initialize()

    documents = [
        Document(
            doc_id="paper-1",
            title="Demo Paper",
            text="Retrieval-Augmented Generation grounds answers.",
            source="sample",
            domain="ai_paper",
        ),
        Document(
            doc_id="paper-2",
            title="GraphRAG Paper",
            text="Graph retrieval links entities.",
            source="sample",
            domain="ai_paper",
        ),
    ]

    written = store.upsert_documents(documents)

    assert written == 2
    assert store.count_documents() == 2


def test_sqlite_store_returns_documents(tmp_path: Path) -> None:
    store = SQLiteStore(tmp_path / "app.db")
    store.initialize()
    store.upsert_documents(
        [
            Document(
                doc_id="paper-1",
                title="Demo Paper",
                text="Retrieval-Augmented Generation grounds answers.",
                source="sample",
                domain="ai_paper",
            )
        ]
    )

    documents = store.list_documents()

    assert len(documents) == 1
    assert documents[0].doc_id == "paper-1"
