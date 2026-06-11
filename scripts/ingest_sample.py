from __future__ import annotations

from app.ingestion.sample_loader import load_sample_papers


def main() -> None:
    documents = load_sample_papers()
    print(f"Loaded {len(documents)} sample documents. Phase 2 will persist them to SQLite/Qdrant/Neo4j.")


if __name__ == "__main__":
    main()
