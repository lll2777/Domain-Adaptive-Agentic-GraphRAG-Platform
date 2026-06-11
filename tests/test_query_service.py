from pathlib import Path

from app.core.documents import Chunk
from app.retrieval.query_service import run_query
from app.storage.sqlite_store import SQLiteStore


def test_query_uses_chunks_from_sqlite_store(tmp_path: Path) -> None:
    store = SQLiteStore(tmp_path / "app.db")
    store.initialize()
    store.upsert_chunks(
        [
            Chunk(
                chunk_id="paper-1-0",
                doc_id="paper-1",
                text="GraphRAG uses graph retrieval to ground answers.",
                metadata={"paper_id": "paper-1"},
            )
        ]
    )

    result = run_query("What is GraphRAG?", store=store, top_k=3)

    assert result.answer
    assert result.retrieved_chunks
    assert result.retrieved_chunks[0].chunk_id == "paper-1-0"
    assert result.citations[0]["chunk_id"] == "paper-1-0"


def test_query_falls_back_to_sample_data_when_store_is_empty(tmp_path: Path) -> None:
    store = SQLiteStore(tmp_path / "app.db")
    store.initialize()

    result = run_query("What is Retrieval-Augmented Generation?", store=store, top_k=3)

    assert result.answer
    assert result.retrieved_chunks
