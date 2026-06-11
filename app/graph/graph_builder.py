from __future__ import annotations

from app.graph.entity_extractor import RuleBasedEntityExtractor
from app.graph.relation_extractor import RuleBasedRelationExtractor
from app.core.documents import Document


def build_graph_records(documents: list[Document]) -> dict[str, list[dict[str, object]]]:
    """Build in-memory graph records from documents."""

    entity_extractor = RuleBasedEntityExtractor()
    relation_extractor = RuleBasedRelationExtractor()
    entities = []
    relations = []
    for document in documents:
        extracted = entity_extractor.extract(document)
        entities.extend(entity.model_dump() for entity in extracted)
        relations.extend(relation.model_dump() for relation in relation_extractor.extract(document, extracted))
    return {"entities": entities, "relations": relations}
