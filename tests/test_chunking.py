from app.core.chunking import chunk_document
from app.core.documents import Document


def test_chunking_returns_non_empty_chunks() -> None:
    document = Document(
        doc_id="paper-1",
        title="Demo Paper",
        text="Retrieval augmented generation combines retrieval and generation for question answering.",
        source="sample",
        domain="ai_paper",
    )

    chunks = chunk_document(document, chunk_size=6, overlap=1)

    assert chunks


def test_chunk_metadata_preserves_doc_id() -> None:
    document = Document(
        doc_id="paper-2",
        title="GraphRAG Demo",
        text="Graph retrieval links methods, datasets, and metrics for grounded answers.",
        source="sample",
        domain="ai_paper",
    )

    chunks = chunk_document(document, chunk_size=5, overlap=0)

    assert chunks[0].doc_id == "paper-2"
    assert chunks[0].metadata["doc_id"] == "paper-2"
