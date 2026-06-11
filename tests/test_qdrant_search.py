import requests

from app.retrieval.qdrant_retriever import QdrantRetriever


class FakeResponse:
    def __init__(self, payload: dict[str, object]) -> None:
        self._payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict[str, object]:
        return self._payload


class FakeSession:
    def post(self, url: str, json: dict[str, object], timeout: int, auth=None) -> FakeResponse:
        if url.endswith("/search"):
            return FakeResponse(
                {
                    "result": [
                        {
                            "id": 1,
                            "score": 0.93,
                            "payload": {
                                "chunk_id": "chunk-1",
                                "doc_id": "paper-1",
                                "text": "GraphRAG uses graph retrieval.",
                                "paper_id": "paper-1",
                            },
                        }
                    ]
                }
            )
        raise AssertionError(f"unexpected url {url}")

    def put(self, url: str, json: dict[str, object], timeout: int) -> FakeResponse:
        return FakeResponse({"status": "ok"})


class FailingSession:
    def post(self, url: str, json: dict[str, object], timeout: int, auth=None) -> FakeResponse:
        raise requests.RequestException("qdrant unavailable")

    def put(self, url: str, json: dict[str, object], timeout: int) -> FakeResponse:
        raise requests.RequestException("qdrant unavailable")


def test_qdrant_search_returns_retrieval_results() -> None:
    retriever = QdrantRetriever(host="localhost", port=6333, session=FakeSession())

    results = retriever.search("GraphRAG", top_k=3)

    assert len(results) == 1
    assert results[0].chunk.chunk_id == "chunk-1"
    assert results[0].score == 0.93


def test_qdrant_search_gracefully_handles_unavailable_service() -> None:
    retriever = QdrantRetriever(host="localhost", port=6333, session=FailingSession())

    results = retriever.search("GraphRAG", top_k=3)

    assert results == []
