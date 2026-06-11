from __future__ import annotations

from app.ingestion.arxiv_loader import ArxivLoader


def main() -> None:
    records = ArxivLoader().fetch("Retrieval-Augmented Generation", categories=["cs.AI", "cs.CL", "cs.IR"], max_results=5)
    print(f"Fetched {len(records)} arXiv metadata records. PDFs were not downloaded.")


if __name__ == "__main__":
    main()
