from pathlib import Path

from app.ingestion.arxiv_loader import ArxivRecord
from app.ingestion.pipeline import ingest_arxiv_records
from app.storage.sqlite_store import SQLiteStore


class FakeQdrantIndexer:
    def __init__(self) -> None:
        self.calls = 0

    def index_chunks(self, chunks):
        self.calls += 1
        return {"status": "ok", "indexed": len(chunks), "message": "Indexed"}


class FakeNeo4jWriter:
    def __init__(self) -> None:
        self.calls = 0

    def write_graph(self, entities, relations):
        self.calls += 1
        return {"status": "ok", "entities": len(entities), "relations": len(relations), "message": "Written"}


def test_arxiv_ingest_persists_metadata_and_routes_followup_steps(tmp_path: Path) -> None:
    store = SQLiteStore(tmp_path / "app.db")
    qdrant = FakeQdrantIndexer()
    neo4j = FakeNeo4jWriter()
    records = [
        ArxivRecord(
            paper_id="2401.00001",
            title="GraphRAG for Retrieval",
            authors=["Ada Lovelace"],
            abstract="GraphRAG improves retrieval quality and citation accuracy.",
            published_date="2024-01-01T00:00:00Z",
            categories=["cs.AI", "cs.IR"],
            pdf_url="https://example.com/demo.pdf",
            source_url="https://arxiv.org/abs/2401.00001",
        )
    ]

    result = ingest_arxiv_records(store, records, qdrant_indexer=qdrant, neo4j_writer=neo4j)

    assert result["status"] == "ok"
    assert result["documents"] == 1
    assert result["chunks"] > 0
    assert result["qdrant_status"] == "ok"
    assert result["neo4j_status"] == "ok"
    assert qdrant.calls == 1
    assert neo4j.calls == 1
    assert store.count_documents() == 1
    stored = store.list_documents()[0]
    assert stored.source == "arxiv"
    assert stored.metadata["authors"] == ["Ada Lovelace"]
    assert stored.metadata["categories"] == ["cs.AI", "cs.IR"]
