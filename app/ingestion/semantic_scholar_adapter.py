from __future__ import annotations


class SemanticScholarAdapter:
    """Skeleton for future citation graph and related-paper metadata."""

    def map_record(self, record: dict[str, object]) -> dict[str, object]:
        return {
            "paper_id": record.get("paperId", ""),
            "title": record.get("title", ""),
            "source_url": record.get("url", ""),
            "metadata": {"provider": "semantic_scholar"},
        }
