from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

from app.core.documents import Chunk
from app.utils.text import tokenize


@dataclass
class RetrievalResult:
    chunk: Chunk
    score: float
    source: str = "bm25"


class BM25Retriever:
    """Tiny BM25 implementation for offline keyword retrieval."""

    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self._chunks: list[Chunk] = []
        self._tokenized: list[list[str]] = []
        self._doc_freq: dict[str, int] = {}
        self._avg_doc_len = 0.0

    def index(self, chunks: Iterable[Chunk]) -> None:
        self._chunks = list(chunks)
        self._tokenized = [tokenize(chunk.text) for chunk in self._chunks]
        self._doc_freq = {}
        for tokens in self._tokenized:
            for token in set(tokens):
                self._doc_freq[token] = self._doc_freq.get(token, 0) + 1
        total_len = sum(len(tokens) for tokens in self._tokenized)
        self._avg_doc_len = total_len / len(self._tokenized) if self._tokenized else 0.0

    def search(self, query: str, top_k: int = 5) -> list[RetrievalResult]:
        query_terms = tokenize(query)
        if not self._chunks or not query_terms:
            return []

        scored: list[RetrievalResult] = []
        total_docs = len(self._chunks)
        for chunk, tokens in zip(self._chunks, self._tokenized):
            score = 0.0
            doc_len = len(tokens) or 1
            for term in query_terms:
                tf = tokens.count(term)
                if tf == 0:
                    continue
                df = self._doc_freq.get(term, 0)
                idf = math.log(1 + (total_docs - df + 0.5) / (df + 0.5))
                denom = tf + self.k1 * (1 - self.b + self.b * doc_len / (self._avg_doc_len or 1))
                score += idf * (tf * (self.k1 + 1)) / denom
            if score > 0:
                scored.append(RetrievalResult(chunk=chunk, score=score))
        return sorted(scored, key=lambda result: result.score, reverse=True)[:top_k]
