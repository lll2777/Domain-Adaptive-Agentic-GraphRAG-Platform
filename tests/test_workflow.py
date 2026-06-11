from app.agent.query_classifier import QueryClassifier
from app.agent.workflow import QueryWorkflow
from app.core.documents import Chunk
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
