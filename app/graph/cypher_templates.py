CYPHER_MERGE_ENTITY = """
MERGE (e:Entity {entity_id: $entity_id})
SET e.name = $name, e.type = $type, e.domain = $domain
"""

CYPHER_MERGE_RELATION = """
MATCH (source:Entity {entity_id: $source_entity})
MATCH (target:Entity {entity_id: $target_entity})
MERGE (source)-[r:RELATED {relation_type: $relation_type}]->(target)
SET r.evidence_chunk_id = $evidence_chunk_id, r.confidence = $confidence
"""
