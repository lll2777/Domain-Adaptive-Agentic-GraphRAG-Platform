from __future__ import annotations

import re


def tokenize(text: str) -> list[str]:
    """Return lowercase word tokens for lightweight retrieval and metrics."""

    return re.findall(r"[a-zA-Z0-9][a-zA-Z0-9_-]*", text.lower())


def keyword_overlap(left: str, right: str) -> float:
    """Compute simple keyword overlap ratio between two strings."""

    left_terms = set(tokenize(left))
    right_terms = set(tokenize(right))
    if not left_terms:
        return 0.0
    return len(left_terms & right_terms) / len(left_terms)
