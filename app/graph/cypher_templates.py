CYPHER_MERGE_ENTITIES = """
UNWIND $entities AS entity
MERGE (e:Entity {entity_id: entity.entity_id})
SET e.name = entity.name,
    e.type = entity.type,
    e.domain = entity.domain,
    e += entity.metadata
"""

CYPHER_MERGE_RELATIONS = """
UNWIND $relations AS relation
MATCH (source:Entity {entity_id: relation.source_entity})
MATCH (target:Entity {entity_id: relation.target_entity})
MERGE (source)-[r:RELATED {relation_type: relation.relation_type}]->(target)
SET r.evidence_chunk_id = relation.evidence_chunk_id,
    r.confidence = relation.confidence,
    r += relation.metadata
"""
