from __future__ import annotations

from app.config import get_settings
from app.ingestion.pipeline import ingest_sample_documents
from app.storage.sqlite_store import SQLiteStore


def main() -> None:
    settings = get_settings()
    store = SQLiteStore(settings.sqlite_path)
    result = ingest_sample_documents(store)
    print(
        f"Loaded {result['documents']} sample documents and {result['chunks']} chunks; "
        f"wrote {result['sqlite_written']} documents and {result['sqlite_chunk_written']} chunks to {settings.sqlite_path}."
    )


if __name__ == "__main__":
    main()
