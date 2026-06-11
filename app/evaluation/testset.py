from __future__ import annotations

import json
from pathlib import Path


def load_sample_questions() -> list[dict[str, str]]:
    path = Path(__file__).resolve().parents[2] / "data" / "eval" / "sample_questions.json"
    return json.loads(path.read_text(encoding="utf-8"))
