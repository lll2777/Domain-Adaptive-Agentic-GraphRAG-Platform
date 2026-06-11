from __future__ import annotations

import json
from pathlib import Path

from app.core.documents import Document


def sample_data_path() -> Path:
    return Path(__file__).resolve().parents[2] / "data" / "samples" / "ai_papers.json"


def load_sample_papers(path: Path | None = None) -> list[Document]:
    """Load bundled synthetic AI paper records as domain-neutral documents."""

    data_path = path or sample_data_path()
    records = json.loads(data_path.read_text(encoding="utf-8"))
    documents: list[Document] = []
    for record in records:
        paper_id = record["paper_id"]
        metadata = dict(record.get("metadata", {}))
        metadata.update(
            {
                "paper_id": paper_id,
                "authors": record.get("authors", []),
                "year": record.get("year"),
                "categories": record.get("categories", []),
                "source_url": record.get("source_url"),
                "pdf_url": record.get("pdf_url"),
                "keywords": record.get("keywords", []),
            }
        )
        text = record.get("abstract", "")
        documents.append(
            Document(
                doc_id=paper_id,
                title=record["title"],
                text=text,
                source=record.get("source_url", "sample"),
                domain="ai_paper",
                metadata=metadata,
            )
        )
    return documents
