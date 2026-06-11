import requests

from app.core.documents import Chunk
from app.retrieval.qdrant_retriever import QdrantRetriever


class FakeResponse:
    def __init__(self, payload: dict[str, object] | None = None) -> None:
        self._payload = payload or {}

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict[str, object]:
        return self._payload


class FakeSession:
    def __init__(self) -> None:
        self.put_calls: list[tuple[str, dict[str, object]]] = []

    def put(self, url: str, json: dict[str, object], timeout: int) -> FakeResponse:
        self.put_calls.append((url, json))
        return FakeResponse({"status": "ok"})


class FailingSession:
    def put(self, url: str, json: dict[str, object], timeout: int) -> FakeResponse:
        raise requests.RequestException("qdrant unavailable")


def test_qdrant_index_chunks_upserts_vectors() -> None:
    session = FakeSession()
    retriever = QdrantRetriever(host="localhost", port=6333, collection_name="test_chunks", session=session)
    chunks = [Chunk(chunk_id="chunk-1", doc_id="paper-1", text="GraphRAG retrieval evidence.")]

    result = retriever.index_chunks(chunks)

    assert result["status"] == "ok"
    assert result["indexed"] == 1
    assert len(session.put_calls) == 2
    assert session.put_calls[0][0].endswith("/collections/test_chunks")
    assert session.put_calls[1][0].endswith("/collections/test_chunks/points?wait=true")
    assert session.put_calls[1][1]["points"][0]["payload"]["chunk_id"] == "chunk-1"


def test_qdrant_index_chunks_gracefully_handles_unavailable_service() -> None:
    retriever = QdrantRetriever(host="localhost", port=6333, collection_name="test_chunks", session=FailingSession())

    result = retriever.index_chunks([Chunk(chunk_id="chunk-1", doc_id="paper-1", text="GraphRAG")])

    assert result["status"] == "unavailable"
    assert result["indexed"] == 0
