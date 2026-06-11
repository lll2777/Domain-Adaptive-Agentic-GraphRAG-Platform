from __future__ import annotations


class RagasAdapter:
    """Placeholder boundary for future RAGAS evaluation integration."""

    def evaluate(self, rows: list[dict[str, object]]) -> dict[str, object]:
        return {
            "status": "planned",
            "adapter": "ragas",
            "items": len(rows),
            "message": "RAGAS is not installed by default; proxy metrics keep the MVP runnable.",
        }


class DeepEvalAdapter:
    """Placeholder boundary for future DeepEval evaluation integration."""

    def evaluate(self, rows: list[dict[str, object]]) -> dict[str, object]:
        return {
            "status": "planned",
            "adapter": "deepeval",
            "items": len(rows),
            "message": "DeepEval is not installed by default; proxy metrics keep the MVP runnable.",
        }
