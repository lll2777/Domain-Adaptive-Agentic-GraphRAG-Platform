from __future__ import annotations

from app.core.documents import Document, Entity
from app.utils.ids import stable_id


METHOD_TERMS = ["rag", "graphrag", "lightrag", "agentic rag", "dense retrieval", "hybrid search", "reranker"]
DATASET_TERMS = ["mmlu", "hotpotqa", "natural questions", "triviaqa", "pubmedqa", "multihop-rag"]
METRIC_TERMS = ["accuracy", "recall", "precision", "faithfulness", "context precision", "latency"]
TASK_TERMS = ["question answering", "multi-hop reasoning", "information retrieval", "summarization"]


class RuleBasedEntityExtractor:
    """Extract simple entities without requiring an LLM."""

    def extract(self, document: Document) -> list[Entity]:
        entities = [
            Entity(
                entity_id=stable_id(document.doc_id, document.title, prefix="entity"),
                name=document.title,
                type="Paper",
                domain=document.domain,
                metadata={"doc_id": document.doc_id},
            )
        ]
        for author in document.metadata.get("authors", []):
            entities.append(
                Entity(
                    entity_id=stable_id(document.doc_id, author, prefix="entity"),
                    name=author,
                    type="Author",
                    domain=document.domain,
                    metadata={"doc_id": document.doc_id},
                )
            )
        lowered = f"{document.title} {document.text}".lower()
        for entity_type, terms in {
            "Method": METHOD_TERMS,
            "Dataset": DATASET_TERMS,
            "Metric": METRIC_TERMS,
            "Task": TASK_TERMS,
        }.items():
            for term in terms:
                if term in lowered:
                    entities.append(
                        Entity(
                            entity_id=stable_id(document.doc_id, entity_type, term, prefix="entity"),
                            name=term,
                            type=entity_type,
                            domain=document.domain,
                            metadata={"doc_id": document.doc_id},
                        )
                    )
        return entities
