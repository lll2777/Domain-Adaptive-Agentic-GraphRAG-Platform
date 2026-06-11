from __future__ import annotations

from typing import Protocol

from app.core.documents import Chunk, Document


class DocumentRepository(Protocol):
    """Repository boundary that SQLite implements today and PostgreSQL can implement later."""

    def upsert_documents(self, documents: list[Document]) -> int:
        """Persist or update documents."""

    def list_documents(self) -> list[Document]:
        """Return stored documents."""


class ChunkRepository(Protocol):
    """Chunk repository boundary for retrieval metadata stores."""

    def upsert_chunks(self, chunks: list[Chunk]) -> int:
        """Persist or update chunks."""

    def list_chunks(self) -> list[Chunk]:
        """Return stored chunks."""
