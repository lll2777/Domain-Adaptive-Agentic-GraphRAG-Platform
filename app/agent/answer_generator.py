from __future__ import annotations

from app.retrieval.bm25_retriever import RetrievalResult


class AnswerGenerator:
    """Generate mock grounded answers from retrieved chunks."""

    def generate(self, question: str, results: list[RetrievalResult]) -> str:
        if not results:
            return "当前证据不足，无法可靠回答。"
        first = results[0].chunk
        paper_id = str(first.metadata.get("paper_id", first.doc_id))
        return (
            f"Based on the retrieved evidence, {question.strip()} can be answered from the available context: "
            f"{first.text} [source: {paper_id}, {first.chunk_id}]"
        )
