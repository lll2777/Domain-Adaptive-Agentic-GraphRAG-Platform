from __future__ import annotations

from fastapi import APIRouter

from app.graph.entity_extractor import RuleBasedEntityExtractor
from app.graph.relation_extractor import RuleBasedRelationExtractor
from app.ingestion.sample_loader import load_sample_papers

router = APIRouter(prefix="/graph", tags=["graph"])


@router.get("/entities")
def get_entities() -> list[dict[str, object]]:
    """Return rule-based sample entities for the demo."""

    extractor = RuleBasedEntityExtractor()
    entities = [entity for document in load_sample_papers() for entity in extractor.extract(document)]
    return [entity.model_dump() for entity in entities]


@router.get("/relations")
def get_relations() -> list[dict[str, object]]:
    """Return rule-based sample relations for the demo."""

    entity_extractor = RuleBasedEntityExtractor()
    relation_extractor = RuleBasedRelationExtractor()
    relations = []
    for document in load_sample_papers():
        relations.extend(relation_extractor.extract(document, entity_extractor.extract(document)))
    return [relation.model_dump() for relation in relations]
