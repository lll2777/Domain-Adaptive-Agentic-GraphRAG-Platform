from __future__ import annotations

from app.agent.workflow import QueryWorkflowResult


def build_score_rows(result: QueryWorkflowResult) -> list[dict[str, float | str]]:
    """Format score fields for the Streamlit sidebar and metrics table."""

    return [
        {"source": "bm25", "score": float(result.scores.get("bm25_score", 0.0))},
        {"source": "qdrant", "score": float(result.scores.get("qdrant_score", 0.0))},
        {"source": "graph", "score": float(result.scores.get("graph_score", 0.0))},
    ]


def build_chunk_rows(result: QueryWorkflowResult) -> list[dict[str, object]]:
    """Flatten retrieved chunks into table rows."""

    rows: list[dict[str, object]] = []
    for chunk in result.retrieved_chunks:
        row = {
            "chunk_id": chunk.chunk_id,
            "doc_id": chunk.doc_id,
            "text": chunk.text,
            "paper_id": chunk.metadata.get("paper_id", ""),
            "title": chunk.metadata.get("title", ""),
        }
        rows.append(row)
    return rows


def build_graph_rows(result: QueryWorkflowResult) -> list[dict[str, object]]:
    """Flatten graph context into display rows."""

    rows: list[dict[str, object]] = []
    for context in result.graph_context:
        rows.append(
            {
                "evidence_chunk_ids": ", ".join(context.get("evidence_chunk_ids", [])),
                "score": context.get("score", 0.0),
                "entities": ", ".join(entity.get("name", "") for entity in context.get("entities", [])),
                "relations": ", ".join(relation.get("relation_type", "") for relation in context.get("relations", [])),
            }
        )
    return rows


def evidence_message(result: QueryWorkflowResult) -> str:
    """Return a short evidence status message for the UI."""

    if result.answer == "当前证据不足，无法可靠回答。":
        return "Evidence insufficient."
    return "Evidence sufficient."


def build_eval_summary_rows(evaluation: dict[str, object]) -> list[dict[str, object]]:
    """Flatten evaluation summary values into display rows."""

    summary = evaluation.get("summary", {})
    if not isinstance(summary, dict):
        return []
    return [{"metric": key, "value": value} for key, value in summary.items()]


def build_eval_metric_rows(evaluation: dict[str, object]) -> list[dict[str, object]]:
    """Return per-question evaluation rows for Streamlit tables."""

    metrics = evaluation.get("metrics", [])
    if not isinstance(metrics, list):
        return []
    return [row for row in metrics if isinstance(row, dict)]
