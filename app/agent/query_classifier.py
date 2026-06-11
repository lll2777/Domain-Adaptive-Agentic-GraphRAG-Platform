from __future__ import annotations


class QueryClassifier:
    """Rule-based first-stage query classifier."""

    def classify(self, question: str) -> str:
        lowered = question.lower()
        if any(term in lowered for term in ["compare", "difference", "versus", " vs "]):
            return "comparison"
        if any(term in lowered for term in ["multi-hop", "multiple hops", "connect", "relationship", "related"]):
            return "multi_hop"
        if any(term in lowered for term in ["trend", "evolution", "from", "over time"]):
            return "trend_analysis"
        if any(term in lowered for term in ["citation", "cite", "evidence supports"]):
            return "citation_trace"
        if any(term in lowered for term in ["weather", "sports", "recipe"]):
            return "out_of_domain"
        return "factual"
