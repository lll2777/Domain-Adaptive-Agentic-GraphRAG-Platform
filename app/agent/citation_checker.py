from __future__ import annotations

import re
from dataclasses import dataclass, field

from app.core.documents import Chunk


@dataclass
class CitationCheckResult:
    is_valid: bool
    citations: list[dict[str, str]] = field(default_factory=list)
    message: str = "OK"


class CitationChecker:
    """Validate that answer citations point to retrieved chunks."""

    _pattern = re.compile(r"\[source:\s*([^,\]]+),\s*([^\]]+)\]", re.IGNORECASE)

    def check(self, answer: str, retrieved_chunks: list[Chunk]) -> CitationCheckResult:
        valid_chunk_ids = {chunk.chunk_id for chunk in retrieved_chunks}
        citations = [
            {"paper_id": match.group(1).strip(), "chunk_id": match.group(2).strip()}
            for match in self._pattern.finditer(answer)
        ]
        if not citations:
            return CitationCheckResult(False, [], "当前证据不足，无法可靠回答。")
        if any(citation["chunk_id"] not in valid_chunk_ids for citation in citations):
            return CitationCheckResult(False, citations, "当前证据不足，无法可靠回答。")
        return CitationCheckResult(True, citations)
