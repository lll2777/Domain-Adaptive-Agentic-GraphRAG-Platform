from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass

import requests


@dataclass
class ArxivRecord:
    paper_id: str
    title: str
    authors: list[str]
    abstract: str
    published_date: str
    categories: list[str]
    pdf_url: str
    source_url: str


class ArxivLoader:
    """Fetch arXiv metadata only; no PDFs are downloaded."""

    api_url = "https://export.arxiv.org/api/query"

    def fetch(self, keyword: str, categories: list[str] | None = None, max_results: int = 50) -> list[ArxivRecord]:
        safe_max = max(1, min(max_results, 50))
        query = f'all:"{keyword}"'
        if categories:
            query += " AND (" + " OR ".join(f"cat:{category}" for category in categories) + ")"
        response = requests.get(
            self.api_url,
            params={"search_query": query, "start": 0, "max_results": safe_max},
            timeout=20,
        )
        response.raise_for_status()
        return self._parse(response.text)

    def _parse(self, xml_text: str) -> list[ArxivRecord]:
        namespace = {"atom": "http://www.w3.org/2005/Atom"}
        root = ET.fromstring(xml_text)
        records: list[ArxivRecord] = []
        for entry in root.findall("atom:entry", namespace):
            source_url = entry.findtext("atom:id", default="", namespaces=namespace)
            paper_id = source_url.rsplit("/", 1)[-1]
            pdf_url = ""
            for link in entry.findall("atom:link", namespace):
                if link.attrib.get("title") == "pdf":
                    pdf_url = link.attrib.get("href", "")
            records.append(
                ArxivRecord(
                    paper_id=paper_id,
                    title=(entry.findtext("atom:title", default="", namespaces=namespace) or "").strip(),
                    authors=[
                        author.findtext("atom:name", default="", namespaces=namespace) or ""
                        for author in entry.findall("atom:author", namespace)
                    ],
                    abstract=(entry.findtext("atom:summary", default="", namespaces=namespace) or "").strip(),
                    published_date=entry.findtext("atom:published", default="", namespaces=namespace) or "",
                    categories=[category.attrib.get("term", "") for category in entry.findall("atom:category", namespace)],
                    pdf_url=pdf_url,
                    source_url=source_url,
                )
            )
        return records
