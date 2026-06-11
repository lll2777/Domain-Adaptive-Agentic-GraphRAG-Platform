import requests

from app.retrieval.graph_retriever import GraphRetrievalResult, GraphRetriever


class FakeResponse:
    def __init__(self, payload: dict[str, object]) -> None:
        self._payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict[str, object]:
        return self._payload


class FakeSession:
    def post(self, url: str, json: dict[str, object], timeout: int, auth=None) -> FakeResponse:
        return FakeResponse(
            {
                "results": [
                    {
                        "data": [
                            {
                                "row": [
                                    {
                                        "entity_id": "paper-1",
                                        "name": "GraphRAG",
                                        "type": "Paper",
                                        "domain": "ai_paper",
                                        "metadata": {},
                                    },
                                    {
                                        "entity_id": "method-1",
                                        "name": "Graph Retrieval",
                                        "type": "Method",
                                        "domain": "ai_paper",
                                        "metadata": {},
                                    },
                                    {
                                        "source_entity": "paper-1",
                                        "target_entity": "method-1",
                                        "relation_type": "PROPOSES",
                                        "evidence_chunk_id": "paper-1-0",
                                        "confidence": 0.8,
                                        "metadata": {},
                                    },
                                ]
                            }
                        ]
                    }
                ],
                "errors": [],
            }
        )


class FailingSession:
    def post(self, url: str, json: dict[str, object], timeout: int, auth=None) -> FakeResponse:
        raise requests.RequestException("neo4j unavailable")


def test_graph_retriever_returns_graph_results() -> None:
    retriever = GraphRetriever(host="localhost", port=7474, session=FakeSession())

    results = retriever.search("GraphRAG", top_k=3)

    assert len(results) == 1
    assert isinstance(results[0], GraphRetrievalResult)
    assert results[0].evidence_chunk_ids == ["paper-1-0"]
    assert results[0].entities[0]["entity_id"] == "paper-1"


def test_graph_retriever_gracefully_handles_unavailable_service() -> None:
    retriever = GraphRetriever(host="localhost", port=7474, session=FailingSession())

    results = retriever.search("GraphRAG", top_k=3)

    assert results == []
