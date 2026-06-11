from __future__ import annotations

from fastapi import FastAPI

from app.api.routes_eval import router as eval_router
from app.api.routes_graph import router as graph_router
from app.api.routes_ingest import router as ingest_router
from app.api.routes_query import router as query_router

app = FastAPI(title="Domain-Adaptive Agentic GraphRAG Platform", version="0.1.0")


@app.get("/")
def health_check() -> dict[str, str]:
    """Health check for beginners and Docker/local smoke tests."""

    return {"status": "ok", "message": "Domain-Adaptive Agentic GraphRAG Platform is running."}


app.include_router(ingest_router)
app.include_router(query_router)
app.include_router(eval_router)
app.include_router(graph_router)
