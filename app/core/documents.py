from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class Document(BaseModel):
    """A source document from any supported domain."""

    doc_id: str
    title: str
    text: str
    source: str
    domain: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class Chunk(BaseModel):
    """A retrievable piece of a document."""

    chunk_id: str
    doc_id: str
    text: str
    section: str | None = None
    page: int | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class Entity(BaseModel):
    """A graph entity extracted from a document or chunk."""

    entity_id: str
    name: str
    type: str
    domain: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class Relation(BaseModel):
    """A graph relation with evidence back to a chunk."""

    source_entity: str
    target_entity: str
    relation_type: str
    evidence_chunk_id: str | None = None
    confidence: float = 1.0
    metadata: dict[str, Any] = Field(default_factory=dict)
