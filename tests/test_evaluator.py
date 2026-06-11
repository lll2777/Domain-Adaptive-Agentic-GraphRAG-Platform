from app.evaluation.evaluator import run_sample_evaluation


def test_sample_evaluation_returns_summary_and_query_metadata() -> None:
    result = run_sample_evaluation()

    assert result["status"] == "ok"
    assert result["summary"]["questions"] == len(result["metrics"])
    assert 0.0 <= result["summary"]["average_citation_accuracy"] <= 1.0

    first_row = result["metrics"][0]
    assert first_row["query_type"]
    assert first_row["retrieved_chunks"] >= 0
    assert {"top_score", "bm25_score", "qdrant_score", "graph_score"}.issubset(first_row)
