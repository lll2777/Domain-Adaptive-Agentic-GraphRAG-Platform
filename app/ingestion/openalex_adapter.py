from __future__ import annotations


class OpenAlexAdapter:
    """Skeleton for future citation, venue, author, and institution metadata."""

    def map_record(self, record: dict[str, object]) -> dict[str, object]:
        return {
            "paper_id": record.get("id", ""),
            "title": record.get("title", ""),
            "source_url": record.get("id", ""),
            "metadata": {"provider": "openalex"},
        }
