from __future__ import annotations

import streamlit as st

from app.core.chunking import chunk_document
from app.config import get_settings
from app.evaluation.evaluator import run_sample_evaluation
from app.graph.neo4j_client import Neo4jClient
from app.graph.graph_builder import build_graph_records
from app.ingestion.pipeline import ingest_sample_documents
from app.ingestion.sample_loader import load_sample_papers
from app.retrieval.qdrant_retriever import QdrantRetriever
from app.retrieval.query_service import run_query
from app.storage.sqlite_store import SQLiteStore
from app.ui.view_models import (
    build_chunk_rows,
    build_eval_metric_rows,
    build_eval_summary_rows,
    build_graph_rows,
    build_graphviz_source,
    build_score_rows,
    evidence_message,
)


def _store() -> SQLiteStore:
    return SQLiteStore(get_settings().sqlite_path)


def _ingest_sample() -> dict[str, int | str]:
    settings = get_settings()
    store = SQLiteStore(settings.sqlite_path)
    qdrant = QdrantRetriever(host=settings.qdrant_host, port=settings.qdrant_port, timeout=2)
    neo4j = Neo4jClient(user=settings.neo4j_user, password=settings.neo4j_password, timeout=2)
    return ingest_sample_documents(store, qdrant_indexer=qdrant, neo4j_writer=neo4j)


st.set_page_config(page_title="Agentic GraphRAG", layout="wide")
st.title("Domain-Adaptive Agentic GraphRAG Platform")

page = st.sidebar.radio("Page", ["Home", "Ingest", "Ask", "Graph", "Evaluation"])
documents = load_sample_papers()
chunks = [chunk for document in documents for chunk in chunk_document(document)]
graph = build_graph_records(documents)

if page == "Home":
    store = _store()
    st.metric("Documents", store.count_documents() or len(documents))
    st.metric("Chunks", store.count_chunks() or len(chunks))
    st.metric("Entities", len(graph["entities"]))
    st.metric("Relations", len(graph["relations"]))
elif page == "Ingest":
    if st.button("Import sample data"):
        result = _ingest_sample()
        st.success(f"Loaded {result['documents']} documents and {result['chunks']} chunks.")
        st.json(result)
    st.info("Sample ingest writes SQLite first, then tries Qdrant and Neo4j. Offline services report unavailable.")
elif page == "Ask":
    question = st.text_input("Question", "What is Retrieval-Augmented Generation?")
    domain = st.selectbox("Domain", ["ai_paper", "financial_report"], index=0)
    top_k = st.slider("Top K", min_value=1, max_value=10, value=5)
    if st.button("Ask"):
        result = run_query(question, store=_store(), domain=domain, top_k=top_k)
        st.subheader("Answer")
        st.write(result.answer)
        summary_cols = st.columns(3)
        summary_cols[0].metric("Query Type", result.query_type)
        summary_cols[1].metric("Evidence", evidence_message(result))
        summary_cols[2].metric("Citations", len(result.citations))

        st.subheader("Retrieval Plan")
        st.write(result.retrieval_plan)
        st.subheader("Source Scores")
        st.dataframe(build_score_rows(result), use_container_width=True)
        st.subheader("Citations")
        st.dataframe(result.citations, use_container_width=True)
        st.subheader("Retrieved Chunks")
        st.dataframe(build_chunk_rows(result), use_container_width=True)
        st.subheader("Graph Context")
        graph_rows = build_graph_rows(result)
        if graph_rows:
            st.dataframe(graph_rows, use_container_width=True)
        else:
            st.info("No graph context returned yet. Start Neo4j and ingest sample data to enable graph retrieval.")
elif page == "Graph":
    st.subheader("Entities")
    st.dataframe(graph["entities"])
    st.subheader("Relations")
    st.dataframe(graph["relations"])
    graphviz_source = build_graphviz_source(graph)
    if graphviz_source:
        st.subheader("Graph View")
        st.graphviz_chart(graphviz_source)
else:
    if st.button("Run sample evaluation"):
        evaluation = run_sample_evaluation()
        st.subheader("Summary")
        st.dataframe(build_eval_summary_rows(evaluation), use_container_width=True)
        st.subheader("Per-Question Metrics")
        st.dataframe(build_eval_metric_rows(evaluation), use_container_width=True)
