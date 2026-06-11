from app.evaluation.adapters import DeepEvalAdapter, RagasAdapter


def test_ragas_adapter_reports_planned_status_without_optional_dependency() -> None:
    result = RagasAdapter().evaluate([])

    assert result["status"] == "planned"
    assert result["adapter"] == "ragas"


def test_deepeval_adapter_reports_planned_status_without_optional_dependency() -> None:
    result = DeepEvalAdapter().evaluate([])

    assert result["status"] == "planned"
    assert result["adapter"] == "deepeval"
