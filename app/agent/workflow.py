from __future__ import annotations

from dataclasses import dataclass, field

from app.agent.answer_generator import AnswerGenerator
from app.agent.citation_checker import CitationChecker
from app.agent.evidence_checker import EvidenceChecker
from app.agent.planner import Planner
from app.agent.query_classifier import QueryClassifier
from app.core.documents import Chunk


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

        try:
            results = self.retriever.search(question, top_k=top_k, domain=domain)
        except TypeError:
            results = self.retriever.search(question, top_k=top_k)
        evidence = self.evidence_checker.check(results)
        if not evidence.is_sufficient:
            return QueryWorkflowResult(
                answer="当前证据不足，无法可靠回答。",
                query_type=query_type,
                retrieval_plan=plan.notes,
                citations=[],
                retrieved_chunks=[],
                scores={"evidence": evidence.message},
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
            scores={"top_score": results[0].score if results else 0.0},
        )
