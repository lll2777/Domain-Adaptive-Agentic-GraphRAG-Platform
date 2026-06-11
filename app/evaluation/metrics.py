from __future__ import annotations

from app.core.documents import Chunk
from app.utils.text import keyword_overlap


def citation_accuracy(citations: list[dict[str, str]], retrieved_chunks: list[Chunk]) -> float:
    if not citations:
        return 0.0
    valid_ids = {chunk.chunk_id for chunk in retrieved_chunks}
    valid = sum(1 for citation in citations if citation.get("chunk_id") in valid_ids)
    return valid / len(citations)


def context_precision_proxy(question: str, retrieved_chunks: list[Chunk]) -> float:
    if not retrieved_chunks:
        return 0.0
    hits = sum(1 for chunk in retrieved_chunks if keyword_overlap(question, chunk.text) > 0)
    return hits / len(retrieved_chunks)


def answer_relevancy_proxy(question: str, answer: str) -> float:
    return keyword_overlap(question, answer)


def faithfulness_proxy(answer: str, retrieved_chunks: list[Chunk]) -> float:
    context = " ".join(chunk.text for chunk in retrieved_chunks)
    return keyword_overlap(answer, context)
