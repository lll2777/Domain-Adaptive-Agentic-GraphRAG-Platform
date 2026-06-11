from __future__ import annotations

import streamlit as st

from app.agent.workflow import QueryWorkflow
from app.core.chunking import chunk_document
from app.evaluation.evaluator import run_sample_evaluation
from app.graph.graph_builder import build_graph_records
from app.ingestion.sample_loader import load_sample_papers
from app.retrieval.bm25_retriever import BM25Retriever


def _build_workflow() -> tuple[QueryWorkflow, list[object]]:
    documents = load_sample_papers()
    chunks = [chunk for document in documents for chunk in chunk_document(document)]
    retriever = BM25Retriever()
    retriever.index(chunks)
    return QueryWorkflow(retriever), chunks


st.set_page_config(page_title="Agentic GraphRAG", layout="wide")
st.title("Domain-Adaptive Agentic GraphRAG Platform")

page = st.sidebar.radio("Page", ["Home", "Ingest", "Ask", "Graph", "Evaluation"])
documents = load_sample_papers()
chunks = [chunk for document in documents for chunk in chunk_document(document)]
graph = build_graph_records(documents)

if page == "Home":
    st.metric("Documents", len(documents))
    st.metric("Chunks", len(chunks))
    st.metric("Entities", len(graph["entities"]))
    st.metric("Relations", len(graph["relations"]))
elif page == "Ingest":
    if st.button("Import sample data"):
        st.success(f"Loaded {len(documents)} sample records in memory.")
    st.info("Qdrant, Neo4j, and SQLite persistence arrive in phase 2. This page is ready for that flow.")
elif page == "Ask":
    question = st.text_input("Question", "What is Retrieval-Augmented Generation?")
    top_k = st.slider("Top K", min_value=1, max_value=10, value=5)
    if st.button("Ask"):
        workflow, _ = _build_workflow()
        result = workflow.run(question, top_k=top_k)
        st.subheader("Answer")
        st.write(result.answer)
        st.subheader("Query Type")
        st.write(result.query_type)
        st.subheader("Retrieval Plan")
        st.write(result.retrieval_plan)
        st.subheader("Citations")
        st.json(result.citations)
        st.subheader("Retrieved Chunks")
        st.json([chunk.model_dump() for chunk in result.retrieved_chunks])
elif page == "Graph":
    st.subheader("Entities")
    st.dataframe(graph["entities"])
    st.subheader("Relations")
    st.dataframe(graph["relations"])
else:
    if st.button("Run sample evaluation"):
        st.json(run_sample_evaluation())
