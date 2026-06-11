from __future__ import annotations

from pydantic import BaseModel, Field
from fastapi import APIRouter

from app.config import get_settings
from app.retrieval.query_service import run_query
from app.storage.sqlite_store import SQLiteStore

router = APIRouter(tags=["query"])


class QueryRequest(BaseModel):
    question: str
    domain: str = "ai_paper"
    top_k: int = Field(default=5, ge=1, le=20)


@router.post("/query")
def query(request: QueryRequest) -> dict[str, object]:
    """Run the query workflow over persisted chunks, with sample fallback."""

    settings = get_settings()
    store = SQLiteStore(settings.sqlite_path)
    result = run_query(request.question, store=store, domain=request.domain, top_k=request.top_k)
    return {
        "answer": result.answer,
        "query_type": result.query_type,
        "retrieval_plan": result.retrieval_plan,
        "citations": result.citations,
        "retrieved_chunks": [chunk.model_dump() for chunk in result.retrieved_chunks],
        "graph_context": result.graph_context,
        "scores": result.scores,
    }
