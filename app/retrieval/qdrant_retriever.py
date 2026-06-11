from __future__ import annotations

import hashlib
from typing import Any, Protocol

import requests

from app.core.documents import Chunk
from app.core.embeddings import HashingEmbeddingModel
from app.retrieval.bm25_retriever import RetrievalResult


class SupportsPut(Protocol):
    def put(self, url: str, json: dict[str, object], timeout: int) -> Any:
        """Protocol for requests-like sessions used by tests and runtime."""


class QdrantRetriever:
    """Qdrant adapter skeleton; first-stage app falls back gracefully if unavailable."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
        collection_name: str = "graphrag_chunks",
        dimensions: int = 128,
        session: SupportsPut | None = None,
        timeout: int = 10,
    ) -> None:
        self.base_url = f"http://{host}:{port}"
        self.collection_name = collection_name
        self.embedding_model = HashingEmbeddingModel(dimensions=dimensions)
        self.dimensions = dimensions
        self.session = session or requests.Session()
        self.timeout = timeout

    def index_chunks(self, chunks: list[Chunk]) -> dict[str, object]:
        """Create a Qdrant collection and upsert chunk vectors.

        If Qdrant is unavailable, return a clear status instead of raising so
        sample ingestion can keep SQLite progress.
        """

        if not chunks:
            return {"status": "ok", "indexed": 0, "message": "No chunks to index."}

        try:
            self._ensure_collection()
            points = [self._point_for_chunk(chunk) for chunk in chunks]
            response = self.session.put(
                f"{self.base_url}/collections/{self.collection_name}/points?wait=true",
                json={"points": points},
                timeout=self.timeout,
            )
            response.raise_for_status()
            return {"status": "ok", "indexed": len(points), "message": "Chunks indexed in Qdrant."}
        except requests.RequestException as exc:
            return {"status": "unavailable", "indexed": 0, "message": f"Qdrant unavailable: {exc}"}

    def search(self, query: str, top_k: int = 5, domain: str | None = None) -> list[RetrievalResult]:
        return []

    def _ensure_collection(self) -> None:
        response = self.session.put(
            f"{self.base_url}/collections/{self.collection_name}",
            json={"vectors": {"size": self.dimensions, "distance": "Cosine"}},
            timeout=self.timeout,
        )
        response.raise_for_status()

    def _point_for_chunk(self, chunk: Chunk) -> dict[str, object]:
        payload = dict(chunk.metadata)
        payload.update({"chunk_id": chunk.chunk_id, "doc_id": chunk.doc_id, "text": chunk.text})
        return {
            "id": self._point_id(chunk.chunk_id),
            "vector": self.embedding_model.embed(chunk.text),
            "payload": payload,
        }

    @staticmethod
    def _point_id(chunk_id: str) -> int:
        digest = hashlib.sha256(chunk_id.encode("utf-8")).digest()
        return int.from_bytes(digest[:8], "big", signed=False)
