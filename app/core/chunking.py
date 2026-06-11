from __future__ import annotations

from app.core.documents import Chunk, Document


def chunk_text(text: str, chunk_size: int = 120, overlap: int = 20) -> list[str]:
    """Split text into word chunks with a small overlap."""

    words = text.split()
    if not words:
        return []
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if overlap < 0:
        raise ValueError("overlap must be non-negative")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks: list[str] = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start = end - overlap
    return chunks


def chunk_document(document: Document, chunk_size: int = 120, overlap: int = 20) -> list[Chunk]:
    """Create retrievable chunks while preserving document metadata."""

    chunk_texts = chunk_text(document.text, chunk_size=chunk_size, overlap=overlap)
    chunks: list[Chunk] = []
    for index, text in enumerate(chunk_texts):
        chunk_id = f"{document.doc_id}-{index}"
        metadata = dict(document.metadata)
        metadata.update({"doc_id": document.doc_id, "title": document.title, "source": document.source})
        chunks.append(
            Chunk(
                chunk_id=chunk_id,
                doc_id=document.doc_id,
                text=text,
                section=metadata.get("section"),
                page=metadata.get("page"),
                metadata=metadata,
            )
        )
    return chunks
