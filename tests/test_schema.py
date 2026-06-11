from app.core.schema import load_domain_schema


def test_ai_paper_schema_loads() -> None:
    schema = load_domain_schema("ai_paper")

    assert schema.domain_name == "ai_paper"
    assert "Paper" in schema.entity_types
    assert "WRITTEN_BY" in schema.relation_types


def test_financial_report_schema_loads() -> None:
    schema = load_domain_schema("financial_report")

    assert schema.domain_name == "financial_report"
    assert "Company" in schema.entity_types
    assert "REPORTS" in schema.relation_types
