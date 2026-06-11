from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Protocol

import requests

from app.utils.text import tokenize

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


@dataclass
class GraphRetrievalResult:
    evidence_chunk_ids: list[str]
    entities: list[dict[str, object]]
    relations: list[dict[str, object]]
    score: float
    source: str = "graph"
    metadata: dict[str, object] = field(default_factory=dict)


class GraphRetriever:
    """Neo4j graph retrieval adapter with graceful fallback."""

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
        self._unavailable = False

    def search(self, query: str, top_k: int = 5) -> list[GraphRetrievalResult]:
        if self._unavailable:
            return []

        terms = [term for term in tokenize(query) if len(term) > 2][:5]
        if not terms:
            return []

        body = {
            "statements": [
                {
                    "statement": """
                    MATCH (source:Entity)-[r:RELATED]->(target:Entity)
                    WHERE any(term IN $terms WHERE
                        toLower(coalesce(source.name, '')) CONTAINS term OR
                        toLower(coalesce(target.name, '')) CONTAINS term)
                    RETURN
                        {
                            entity_id: source.entity_id,
                            name: source.name,
                            type: source.type,
                            domain: source.domain,
                            metadata: properties(source)
                        } AS source_entity,
                        {
                            entity_id: target.entity_id,
                            name: target.name,
                            type: target.type,
                            domain: target.domain,
                            metadata: properties(target)
                        } AS target_entity,
                        {
                            source_entity: source.entity_id,
                            target_entity: target.entity_id,
                            relation_type: r.relation_type,
                            evidence_chunk_id: r.evidence_chunk_id,
                            confidence: r.confidence,
                            metadata: properties(r)
                        } AS relation
                    LIMIT $limit
                    """,
                    "parameters": {"terms": terms, "limit": top_k},
                }
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
            return self._parse_results(payload, terms, top_k)
        except requests.RequestException as exc:
            self._unavailable = True
            logger.info("Neo4j graph retrieval unavailable: %s", exc)
            return []

    def _parse_results(self, payload: dict[str, object], terms: list[str], top_k: int) -> list[GraphRetrievalResult]:
        graph_results: list[GraphRetrievalResult] = []
        for result in payload.get("results", []):
            for data_row in result.get("data", []):
                row = data_row.get("row", [])
                if len(row) != 3:
                    continue
                source_entity = row[0] if isinstance(row[0], dict) else {}
                target_entity = row[1] if isinstance(row[1], dict) else {}
                relation = row[2] if isinstance(row[2], dict) else {}
                evidence_chunk_id = str(relation.get("evidence_chunk_id", ""))
                graph_results.append(
                    GraphRetrievalResult(
                        evidence_chunk_ids=[evidence_chunk_id] if evidence_chunk_id else [],
                        entities=[source_entity, target_entity],
                        relations=[relation],
                        score=float(relation.get("confidence", 0.5) or 0.5),
                        metadata={"query_terms": terms},
                    )
                )
        return graph_results[:top_k]
