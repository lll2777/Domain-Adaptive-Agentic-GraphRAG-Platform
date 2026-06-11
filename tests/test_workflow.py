from app.agent.query_classifier import QueryClassifier
from app.agent.workflow import QueryWorkflow
from app.core.documents import Chunk
from app.retrieval.bm25_retriever import RetrievalResult
from app.retrieval.bm25_retriever import BM25Retriever


def test_query_classifier_identifies_core_types() -> None:
    classifier = QueryClassifier()

    assert classifier.classify("What is Retrieval-Augmented Generation?") == "factual"
    assert classifier.classify("Compare GraphRAG and vector RAG.") == "comparison"
    assert classifier.classify("How does GraphRAG connect papers to datasets over multiple hops?") == "multi_hop"


def test_workflow_mock_mode_returns_answer_and_citations() -> None:
    chunks = [
        Chunk(
            chunk_id="paper-1-0",
            doc_id="paper-1",
            text="Retrieval-Augmented Generation grounds answers in retrieved evidence.",
            metadata={"paper_id": "paper-1"},
        )
    ]
    retriever = BM25Retriever()
    retriever.index(chunks)
    workflow = QueryWorkflow(retriever=retriever)

    result = workflow.run("What is Retrieval-Augmented Generation?", domain="ai_paper", top_k=1)

    assert result.answer
    assert result.citations
    assert result.citations[0]["chunk_id"] == "paper-1-0"


class RetryRetriever:
    def __init__(self) -> None:
        self.queries: list[str] = []
        self.chunk = Chunk(
            chunk_id="paper-2-0",
            doc_id="paper-2",
            text="GraphRAG improves multi-hop retrieval with graph context.",
            metadata={"paper_id": "paper-2"},
        )

    def search(self, query: str, top_k: int = 5, domain: str | None = None):
        self.queries.append(query)
        if len(self.queries) == 1:
            return []
        return [RetrievalResult(chunk=self.chunk, score=0.8, source="bm25")]


def test_workflow_rewrites_query_once_when_evidence_is_missing() -> None:
    retriever = RetryRetriever()
    workflow = QueryWorkflow(retriever=retriever)

    result = workflow.run("GraphRAG?", domain="ai_paper", top_k=1)

    assert len(retriever.queries) == 2
    assert retriever.queries[1] != "GraphRAG?"
    assert result.citations[0]["chunk_id"] == "paper-2-0"
    assert result.scores["rewrite_attempted"] == 1
