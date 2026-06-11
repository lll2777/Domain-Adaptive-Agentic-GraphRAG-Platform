from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RetrievalPlan:
    query_type: str
    retrievers: list[str]
    notes: str


class Planner:
    """Map query types to retrieval strategies."""

    def plan(self, query_type: str) -> RetrievalPlan:
        mapping = {
            "factual": ["bm25", "vector"],
            "comparison": ["bm25", "vector", "graph"],
            "multi_hop": ["graph", "vector"],
            "trend_analysis": ["graph", "vector"],
            "citation_trace": ["graph"],
            "out_of_domain": [],
        }
        retrievers = mapping.get(query_type, ["bm25"])
        notes = "Out of domain or insufficient data." if not retrievers else "Use " + " + ".join(retrievers)
        return RetrievalPlan(query_type=query_type, retrievers=retrievers, notes=notes)
