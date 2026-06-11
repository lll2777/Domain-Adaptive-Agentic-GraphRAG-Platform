from __future__ import annotations


class GraphRetriever:
    """Neo4j graph retrieval skeleton with graceful fallback."""

    def search(self, query: str, top_k: int = 5) -> list[dict[str, object]]:
        return []
