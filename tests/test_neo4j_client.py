import requests

from app.graph.neo4j_client import Neo4jClient


class FakeResponse:
    def __init__(self, payload: dict[str, object] | None = None) -> None:
        self._payload = payload or {"errors": []}

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict[str, object]:
        return self._payload


class FakeSession:
    def __init__(self) -> None:
        self.post_calls: list[tuple[str, dict[str, object], tuple[str, str] | None]] = []

    def post(
        self,
        url: str,
        json: dict[str, object],
        timeout: int,
        auth: tuple[str, str] | None = None,
    ) -> FakeResponse:
        self.post_calls.append((url, json, auth))
        return FakeResponse()


class FailingSession:
    def post(
        self,
        url: str,
        json: dict[str, object],
        timeout: int,
        auth: tuple[str, str] | None = None,
    ) -> FakeResponse:
        raise requests.RequestException("neo4j unavailable")


def test_neo4j_client_writes_graph_records() -> None:
    session = FakeSession()
    client = Neo4jClient(host="localhost", port=7474, user="neo4j", password="secret", session=session)
    entities = [{"entity_id": "e1", "name": "GraphRAG", "type": "Method", "domain": "ai_paper", "metadata": {}}]
    relations = [
        {
            "source_entity": "paper-1",
            "target_entity": "e1",
            "relation_type": "PROPOSES",
            "evidence_chunk_id": "paper-1-0",
            "confidence": 0.8,
            "metadata": {},
        }
    ]

    result = client.write_graph(entities, relations)

    assert result["status"] == "ok"
    assert result["entities"] == 1
    assert result["relations"] == 1
    assert len(session.post_calls) == 1
    url, body, auth = session.post_calls[0]
    assert url.endswith("/db/neo4j/tx/commit")
    assert auth == ("neo4j", "secret")
    assert len(body["statements"]) == 2
    assert body["statements"][0]["parameters"]["entities"][0]["entity_id"] == "e1"


def test_neo4j_client_gracefully_handles_unavailable_service() -> None:
    client = Neo4jClient(host="localhost", port=7474, user="neo4j", password="secret", session=FailingSession())

    result = client.write_graph([{"entity_id": "e1"}], [])

    assert result["status"] == "unavailable"
    assert result["entities"] == 0
    assert result["relations"] == 0
