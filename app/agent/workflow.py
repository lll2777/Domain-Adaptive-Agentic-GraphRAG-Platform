from __future__ import annotations

from dataclasses import dataclass, field

from app.agent.answer_generator import AnswerGenerator
from app.agent.citation_checker import CitationChecker
from app.agent.evidence_checker import EvidenceChecker
from app.agent.planner import Planner
from app.agent.query_classifier import QueryClassifier
from app.core.documents import Chunk
from app.retrieval.bm25_retriever import RetrievalResult


@dataclass
class QueryWorkflowResult:
    answer: str
    query_type: str
    retrieval_plan: str
    citations: list[dict[str, str]]
    retrieved_chunks: list[Chunk]
    graph_context: list[dict[str, object]] = field(default_factory=list)
    scores: dict[str, float | int | str] = field(default_factory=dict)


class QueryWorkflow:
    """Lightweight agentic workflow that can later be replaced by LangGraph."""

    def __init__(self, retriever: object) -> None:
        self.retriever = retriever
        self.classifier = QueryClassifier()
        self.planner = Planner()
        self.evidence_checker = EvidenceChecker()
        self.answer_generator = AnswerGenerator()
        self.citation_checker = CitationChecker()

    def run(self, question: str, domain: str = "ai_paper", top_k: int = 5) -> QueryWorkflowResult:
        query_type = self.classifier.classify(question)
        plan = self.planner.plan(query_type)
        if query_type == "out_of_domain":
            return QueryWorkflowResult(
                answer="当前问题超出已加载领域数据范围，无法可靠回答。",
                query_type=query_type,
                retrieval_plan=plan.notes,
                citations=[],
                retrieved_chunks=[],
            )

        results = self._search(question, top_k=top_k, domain=domain)
        evidence = self.evidence_checker.check(results)
        if not evidence.is_sufficient:
            rewritten_question = self._rewrite_query(question, query_type, domain)
            results = self._search(rewritten_question, top_k=top_k, domain=domain)
            evidence = self.evidence_checker.check(results)
            if not evidence.is_sufficient:
                return QueryWorkflowResult(
                    answer="当前证据不足，无法可靠回答。",
                    query_type=query_type,
                    retrieval_plan=plan.notes,
                    citations=[],
                    retrieved_chunks=[],
                    scores={"evidence": evidence.message, "rewrite_attempted": 1, "rewritten_query": rewritten_question},
                )

        chunks = [result.chunk for result in results]
        answer = self.answer_generator.generate(question, results)
        citation_result = self.citation_checker.check(answer, chunks)
        if not citation_result.is_valid:
            answer = citation_result.message
        return QueryWorkflowResult(
            answer=answer,
            query_type=query_type,
            retrieval_plan=plan.notes,
            citations=citation_result.citations if citation_result.is_valid else [],
            retrieved_chunks=chunks,
            graph_context=[],
            scores={"top_score": results[0].score if results else 0.0, "rewrite_attempted": 1 if "rewritten_question" in locals() else 0},
        )

    def _search(self, question: str, top_k: int, domain: str) -> list[RetrievalResult]:
        try:
            return self.retriever.search(question, top_k=top_k, domain=domain)
        except TypeError:
            return self.retriever.search(question, top_k=top_k)

    def _rewrite_query(self, question: str, query_type: str, domain: str) -> str:
        """Rewrite once with retrieval-oriented context when initial evidence is missing."""

        return f"{question.strip()} domain {domain} {query_type} evidence keywords"
