from __future__ import annotations

from app.agent.workflow import QueryWorkflow
from app.core.chunking import chunk_document
from app.evaluation.metrics import (
    answer_relevancy_proxy,
    citation_accuracy,
    context_precision_proxy,
    faithfulness_proxy,
)
from app.evaluation.testset import load_sample_questions
from app.ingestion.sample_loader import load_sample_papers
from app.retrieval.bm25_retriever import BM25Retriever


def run_sample_evaluation() -> dict[str, object]:
    documents = load_sample_papers()
    chunks = [chunk for document in documents for chunk in chunk_document(document)]
    retriever = BM25Retriever()
    retriever.index(chunks)
    workflow = QueryWorkflow(retriever=retriever)

    rows = []
    for item in load_sample_questions():
        question = item["question"]
        result = workflow.run(question, domain="ai_paper", top_k=5)
        rows.append(
            {
                "question": question,
                "answer_relevancy_proxy": answer_relevancy_proxy(question, result.answer),
                "context_precision_proxy": context_precision_proxy(question, result.retrieved_chunks),
                "citation_accuracy": citation_accuracy(result.citations, result.retrieved_chunks),
                "faithfulness_proxy": faithfulness_proxy(result.answer, result.retrieved_chunks),
            }
        )
    return {"status": "ok", "metrics": rows}
