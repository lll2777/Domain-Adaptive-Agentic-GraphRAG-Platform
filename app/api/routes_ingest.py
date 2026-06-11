from __future__ import annotations

from fastapi import APIRouter

from app.ingestion.sample_loader import load_sample_papers

router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("/sample")
def ingest_sample() -> dict[str, object]:
    """Load bundled sample metadata for the first-stage demo."""

    documents = load_sample_papers()
    return {"status": "ok", "documents": len(documents), "message": "Sample records loaded in memory."}


@router.post("/arxiv")
def ingest_arxiv(keyword: str = "Retrieval-Augmented Generation", max_results: int = 50) -> dict[str, object]:
    """Return a safe placeholder for arXiv ingest until phase 2 persists data."""

    return {
        "status": "planned",
        "keyword": keyword,
        "max_results": min(max_results, 50),
        "message": "arXiv metadata loader skeleton is available; persistence arrives in phase 2.",
    }
