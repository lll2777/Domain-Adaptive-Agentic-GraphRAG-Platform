from __future__ import annotations

from dataclasses import dataclass

from app.retrieval.bm25_retriever import RetrievalResult


@dataclass
class EvidenceCheckResult:
    is_sufficient: bool
    message: str


class EvidenceChecker:
    """Check whether retrieval returned enough evidence for an answer."""

    def check(self, results: list[RetrievalResult]) -> EvidenceCheckResult:
        if not results:
            return EvidenceCheckResult(False, "No retrieved chunks were found.")
        return EvidenceCheckResult(True, "Retrieved evidence is available.")
