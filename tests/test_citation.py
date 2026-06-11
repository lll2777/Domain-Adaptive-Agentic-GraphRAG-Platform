from app.agent.citation_checker import CitationChecker
from app.core.documents import Chunk


def test_citation_checker_accepts_valid_reference() -> None:
    checker = CitationChecker()
    chunks = [Chunk(chunk_id="chunk-1", doc_id="paper-1", text="Grounded evidence.")]
    answer = "This answer is grounded. [source: paper-1, chunk-1]"

    result = checker.check(answer, chunks)

    assert result.is_valid
    assert result.citations[0]["chunk_id"] == "chunk-1"


def test_citation_checker_rejects_fabricated_reference() -> None:
    checker = CitationChecker()
    chunks = [Chunk(chunk_id="chunk-1", doc_id="paper-1", text="Grounded evidence.")]
    answer = "This answer cites missing evidence. [source: paper-9, chunk-9]"

    result = checker.check(answer, chunks)

    assert not result.is_valid
    assert result.message == "当前证据不足，无法可靠回答。"
