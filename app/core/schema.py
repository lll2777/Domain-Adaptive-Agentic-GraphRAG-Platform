from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class DomainSchema(BaseModel):
    """Configuration describing entities, relations, retrieval, and evaluation for a domain."""

    domain_name: str
    entity_types: list[str]
    relation_types: list[str]
    metadata_fields: list[str] = Field(default_factory=list)
    default_retrievers: list[str] = Field(default_factory=list)
    evaluation_metrics: list[str] = Field(default_factory=list)


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_domain_schema(domain_name: str, config_dir: Path | None = None) -> DomainSchema:
    """Load a domain schema from configs/domains/<domain_name>.yaml."""

    try:
        import yaml
    except ImportError as exc:  # pragma: no cover - requirements include PyYAML.
        raise RuntimeError("PyYAML is required to load domain schemas. Run `pip install -r requirements.txt`.") from exc

    base_dir = config_dir or _project_root() / "configs" / "domains"
    schema_path = base_dir / f"{domain_name}.yaml"
    if not schema_path.exists():
        raise FileNotFoundError(f"Domain schema not found: {schema_path}")

    data: dict[str, Any] = yaml.safe_load(schema_path.read_text(encoding="utf-8")) or {}
    return DomainSchema(**data)
