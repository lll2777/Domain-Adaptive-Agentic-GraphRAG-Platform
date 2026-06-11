from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class Neo4jClient:
    """Neo4j client placeholder with graceful no-driver fallback."""

    def is_available(self) -> bool:
        return False

    def write_graph(self, entities: list[dict[str, object]], relations: list[dict[str, object]]) -> dict[str, object]:
        logger.info("Neo4j write skipped in phase 1: %s entities, %s relations", len(entities), len(relations))
        return {"status": "skipped", "entities": len(entities), "relations": len(relations)}
