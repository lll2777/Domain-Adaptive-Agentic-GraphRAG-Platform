from __future__ import annotations

import logging
from typing import Any, Protocol

import requests

from app.graph.cypher_templates import CYPHER_MERGE_ENTITIES, CYPHER_MERGE_RELATIONS

logger = logging.getLogger(__name__)


class SupportsPost(Protocol):
    def post(
        self,
        url: str,
        json: dict[str, object],
        timeout: int,
        auth: tuple[str, str] | None = None,
    ) -> Any:
        """Protocol for requests-like sessions used by tests and runtime."""


class Neo4jClient:
    """Neo4j HTTP transaction client with graceful fallback."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 7474,
        user: str = "neo4j",
        password: str = "please_change_me",
        database: str = "neo4j",
        session: SupportsPost | None = None,
        timeout: int = 10,
    ) -> None:
        self.base_url = f"http://{host}:{port}"
        self.user = user
        self.password = password
        self.database = database
        self.session = session or requests.Session()
        self.timeout = timeout

    def is_available(self) -> bool:
        return True

    def write_graph(self, entities: list[dict[str, object]], relations: list[dict[str, object]]) -> dict[str, object]:
        """Write entity and relation records through Neo4j's transactional HTTP endpoint."""

        if not entities and not relations:
            return {"status": "ok", "entities": 0, "relations": 0, "message": "No graph records to write."}

        body = {
            "statements": [
                {
                    "statement": CYPHER_MERGE_ENTITIES,
                    "parameters": {"entities": entities},
                },
                {
                    "statement": CYPHER_MERGE_RELATIONS,
                    "parameters": {"relations": relations},
                },
            ]
        }
        try:
            response = self.session.post(
                f"{self.base_url}/db/{self.database}/tx/commit",
                json=body,
                timeout=self.timeout,
                auth=(self.user, self.password),
            )
            response.raise_for_status()
            payload = response.json()
            if payload.get("errors"):
                raise requests.RequestException(str(payload["errors"]))
            return {
                "status": "ok",
                "entities": len(entities),
                "relations": len(relations),
                "message": "Graph records written to Neo4j.",
            }
        except requests.RequestException as exc:
            logger.info("Neo4j write skipped because service is unavailable: %s", exc)
            return {
                "status": "unavailable",
                "entities": 0,
                "relations": 0,
                "message": f"Neo4j unavailable: {exc}",
            }
