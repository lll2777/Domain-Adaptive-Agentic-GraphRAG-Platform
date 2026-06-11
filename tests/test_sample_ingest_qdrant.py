from pathlib import Path

from app.core.documents import Chunk
from app.ingestion.pipeline import ingest_sample_documents
from app.storage.sqlite_store import SQLiteStore


class FakeQdrantIndexer:
    def __init__(self) -> None:
        self.calls: list[list[Chunk]] = []

    def index_chunks(self, chunks: list[Chunk]) -> dict[str, object]:
        self.calls.append(chunks)
        return {"status": "ok", "indexed": len(chunks), "message": "Indexed"}


def test_sample_ingest_reports_qdrant_status(tmp_path: Path) -> None:
    store = SQLiteStore(tmp_path / "app.db")
    qdrant = FakeQdrantIndexer()

    result = ingest_sample_documents(store, qdrant_indexer=qdrant)

    assert result["qdrant_status"] == "ok"
    assert result["qdrant_indexed"] == result["chunks"]
    assert len(qdrant.calls) == 1
