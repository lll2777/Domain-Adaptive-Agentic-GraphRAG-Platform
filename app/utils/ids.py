from __future__ import annotations

import hashlib


def stable_id(*parts: str, prefix: str = "id") -> str:
    """Create a stable short ID from text parts."""

    digest = hashlib.sha1("::".join(parts).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}-{digest}"
