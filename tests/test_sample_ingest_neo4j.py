from pathlib import Path

from app.ingestion.pipeline import ingest_sample_documents
from app.storage.sqlite_store import SQLiteStore


class FakeNeo4jWriter:
    def __init__(self) -> None:
        self.calls: list[tuple[list[dict[str, object]], list[dict[str, object]]]] = []

    def write_graph(self, entities: list[dict[str, object]], relations: list[dict[str, object]]) -> dict[str, object]:
        self.calls.append((entities, relations))
        return {"status": "ok", "entities": len(entities), "relations": len(relations), "message": "Written"}


def test_sample_ingest_reports_neo4j_status(tmp_path: Path) -> None:
    store = SQLiteStore(tmp_path / "app.db")
    neo4j = FakeNeo4jWriter()

    result = ingest_sample_documents(store, neo4j_writer=neo4j)

    assert result["neo4j_status"] == "ok"
    assert result["neo4j_entities"] > 0
    assert result["neo4j_relations"] > 0
    assert len(neo4j.calls) == 1
