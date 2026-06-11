from __future__ import annotations

from app.core.chunking import chunk_document
from app.core.documents import Chunk, Document


def build_chunks(documents: list[Document]) -> list[Chunk]:
    """Chunk documents for retrieval and future persistence."""

    return [chunk for document in documents for chunk in chunk_document(document)]
