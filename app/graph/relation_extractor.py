from __future__ import annotations

from app.core.documents import Document, Entity, Relation


class RuleBasedRelationExtractor:
    """Create simple paper-author and paper-method relations."""

    def extract(self, document: Document, entities: list[Entity]) -> list[Relation]:
        paper = next((entity for entity in entities if entity.type == "Paper"), None)
        if not paper:
            return []
        relations: list[Relation] = []
        for entity in entities:
            if entity.entity_id == paper.entity_id:
                continue
            relation_type = "WRITTEN_BY" if entity.type == "Author" else "MENTIONS"
            if entity.type == "Method":
                relation_type = "PROPOSES"
            if entity.type == "Dataset":
                relation_type = "EVALUATES_ON"
            relations.append(
                Relation(
                    source_entity=paper.entity_id,
                    target_entity=entity.entity_id,
                    relation_type=relation_type,
                    evidence_chunk_id=f"{document.doc_id}-0",
                    confidence=0.7,
                    metadata={"doc_id": document.doc_id},
                )
            )
        return relations
