from pathlib import Path

from app.ingestion.pipeline import ingest_sample_documents
from app.storage.sqlite_store import SQLiteStore


def test_sample_ingest_writes_chunks_to_sqlite(tmp_path: Path) -> None:
    store = SQLiteStore(tmp_path / "app.db")

    result = ingest_sample_documents(store)

    assert result["chunks"] > 0
    assert result["sqlite_chunk_written"] == result["chunks"]
    assert store.count_chunks() == result["chunks"]
