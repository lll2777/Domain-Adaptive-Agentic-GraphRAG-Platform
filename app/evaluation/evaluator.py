from __future__ import annotations

from app.config import get_settings
from app.agent.workflow import QueryWorkflow, QueryWorkflowResult
from app.evaluation.metrics import (
    answer_relevancy_proxy,
    citation_accuracy,
    context_precision_proxy,
    faithfulness_proxy,
)
from app.evaluation.testset import load_sample_questions
from app.retrieval.hybrid_retriever import HybridRetriever
from app.retrieval.query_service import build_hybrid_retriever
from app.storage.sqlite_store import SQLiteStore


METRIC_KEYS = [
    "answer_relevancy_proxy",
    "context_precision_proxy",
    "citation_accuracy",
    "faithfulness_proxy",
]


def run_sample_evaluation() -> dict[str, object]:
    store = SQLiteStore(get_settings().sqlite_path)
    retriever = build_hybrid_retriever(store)
    workflow = QueryWorkflow(retriever=retriever)

    rows = []
    for item in load_sample_questions():
        question = item["question"]
        result = _run_with_retriever(question, workflow, retriever)
        rows.append(
            {
                "question": question,
                "query_type": result.query_type,
                "retrieval_plan": result.retrieval_plan,
                "retrieved_chunks": len(result.retrieved_chunks),
                "citations": len(result.citations),
                "top_score": float(result.scores.get("top_score", 0.0)),
                "bm25_score": float(result.scores.get("bm25_score", 0.0)),
                "qdrant_score": float(result.scores.get("qdrant_score", 0.0)),
                "graph_score": float(result.scores.get("graph_score", 0.0)),
                "answer_relevancy_proxy": answer_relevancy_proxy(question, result.answer),
                "context_precision_proxy": context_precision_proxy(question, result.retrieved_chunks),
                "citation_accuracy": citation_accuracy(result.citations, result.retrieved_chunks),
                "faithfulness_proxy": faithfulness_proxy(result.answer, result.retrieved_chunks),
            }
        )
    return {"status": "ok", "summary": _summarize(rows), "metrics": rows}


def _run_with_retriever(
    question: str,
    workflow: QueryWorkflow,
    retriever: HybridRetriever,
) -> QueryWorkflowResult:
    """Run one evaluation question while reusing the same hybrid retriever."""

    result = workflow.run(question, domain="ai_paper", top_k=5)
    result.graph_context = retriever.last_graph_context
    result.scores.update(
        {
            "bm25_score": retriever.last_source_scores.get("bm25", 0.0),
            "qdrant_score": retriever.last_source_scores.get("qdrant", 0.0),
            "graph_score": retriever.last_source_scores.get("graph", 0.0),
        }
    )
    return result


def _summarize(rows: list[dict[str, object]]) -> dict[str, float | int]:
    """Average evaluation metric rows for a compact dashboard summary."""

    summary: dict[str, float | int] = {"questions": len(rows)}
    for key in METRIC_KEYS:
        summary[f"average_{key}"] = sum(float(row[key]) for row in rows) / len(rows) if rows else 0.0
    return summary
