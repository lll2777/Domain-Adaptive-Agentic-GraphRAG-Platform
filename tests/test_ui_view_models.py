from app.agent.workflow import QueryWorkflowResult
from app.core.documents import Chunk
from app.ui.view_models import (
    build_chunk_rows,
    build_eval_metric_rows,
    build_eval_summary_rows,
    build_graph_rows,
    build_graphviz_source,
    build_score_rows,
    evidence_message,
)


def test_build_score_rows_formats_known_scores() -> None:
    result = QueryWorkflowResult(
        answer="answer",
        query_type="factual",
        retrieval_plan="Use bm25",
        citations=[],
        retrieved_chunks=[],
        scores={"bm25_score": 0.5, "qdrant_score": 0.0, "graph_score": 0.25},
    )

    rows = build_score_rows(result)

    assert rows == [
        {"source": "bm25", "score": 0.5},
        {"source": "qdrant", "score": 0.0},
        {"source": "graph", "score": 0.25},
    ]


def test_build_chunk_rows_keeps_citation_fields() -> None:
    result = QueryWorkflowResult(
        answer="answer",
        query_type="factual",
        retrieval_plan="Use bm25",
        citations=[],
        retrieved_chunks=[
            Chunk(
                chunk_id="chunk-1",
                doc_id="paper-1",
                text="GraphRAG uses graph retrieval.",
                metadata={"paper_id": "paper-1", "title": "GraphRAG Demo"},
            )
        ],
    )

    rows = build_chunk_rows(result)

    assert rows[0]["chunk_id"] == "chunk-1"
    assert rows[0]["paper_id"] == "paper-1"
    assert rows[0]["title"] == "GraphRAG Demo"


def test_build_graph_rows_flattens_context() -> None:
    result = QueryWorkflowResult(
        answer="answer",
        query_type="comparison",
        retrieval_plan="Use graph",
        citations=[],
        retrieved_chunks=[],
        graph_context=[
            {
                "evidence_chunk_ids": ["chunk-1"],
                "score": 0.8,
                "entities": [{"name": "GraphRAG"}, {"name": "RAG"}],
                "relations": [{"relation_type": "COMPARES_WITH"}],
            }
        ],
    )

    rows = build_graph_rows(result)

    assert rows == [
        {
            "evidence_chunk_ids": "chunk-1",
            "score": 0.8,
            "entities": "GraphRAG, RAG",
            "relations": "COMPARES_WITH",
        }
    ]


def test_evidence_message_reports_missing_evidence() -> None:
    result = QueryWorkflowResult(
        answer="当前证据不足，无法可靠回答。",
        query_type="factual",
        retrieval_plan="Use bm25",
        citations=[],
        retrieved_chunks=[],
    )

    assert evidence_message(result) == "Evidence insufficient."


def test_eval_rows_flatten_summary_and_metrics() -> None:
    evaluation = {
        "summary": {
            "questions": 2,
            "average_answer_relevancy_proxy": 0.4,
            "average_context_precision_proxy": 0.5,
            "average_citation_accuracy": 1.0,
            "average_faithfulness_proxy": 0.75,
        },
        "metrics": [
            {
                "question": "What is RAG?",
                "query_type": "factual",
                "retrieved_chunks": 3,
                "citations": 1,
                "answer_relevancy_proxy": 0.4,
                "context_precision_proxy": 0.5,
                "citation_accuracy": 1.0,
                "faithfulness_proxy": 0.75,
            }
        ],
    }

    assert build_eval_summary_rows(evaluation)[0] == {"metric": "questions", "value": 2}
    assert build_eval_metric_rows(evaluation)[0]["question"] == "What is RAG?"


def test_build_graphviz_source_renders_entities_and_relations() -> None:
    graph = {
        "entities": [
            {"entity_id": "paper-1", "name": "GraphRAG", "type": "Paper"},
            {"entity_id": "method-1", "name": "Graph Retrieval", "type": "Method"},
        ],
        "relations": [
            {
                "source_entity": "paper-1",
                "target_entity": "method-1",
                "relation_type": "PROPOSES",
                "evidence_chunk_id": "chunk-1",
            }
        ],
    }

    source = build_graphviz_source(graph)

    assert "GraphRAG" in source
    assert "Graph Retrieval" in source
    assert "PROPOSES" in source
