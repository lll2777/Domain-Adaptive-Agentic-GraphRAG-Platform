from __future__ import annotations

from pydantic import BaseModel, Field
from fastapi import APIRouter

from app.core.chunking import chunk_document
from app.ingestion.sample_loader import load_sample_papers
from app.retrieval.bm25_retriever import BM25Retriever
from app.agent.workflow import QueryWorkflow

router = APIRouter(tags=["query"])


class QueryRequest(BaseModel):
    question: str
    domain: str = "ai_paper"
    top_k: int = Field(default=5, ge=1, le=20)


@router.post("/query")
def query(request: QueryRequest) -> dict[str, object]:
    """Run a mock-friendly local query workflow over bundled sample data."""

    documents = load_sample_papers()
    chunks = [chunk for document in documents for chunk in chunk_document(document)]
    retriever = BM25Retriever()
    retriever.index(chunks)
    result = QueryWorkflow(retriever=retriever).run(request.question, domain=request.domain, top_k=request.top_k)
    return {
        "answer": result.answer,
        "query_type": result.query_type,
        "retrieval_plan": result.retrieval_plan,
        "citations": result.citations,
        "retrieved_chunks": [chunk.model_dump() for chunk in result.retrieved_chunks],
        "graph_context": result.graph_context,
        "scores": result.scores,
    }
