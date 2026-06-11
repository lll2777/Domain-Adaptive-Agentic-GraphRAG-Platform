from __future__ import annotations

from fastapi import APIRouter

from app.evaluation.evaluator import run_sample_evaluation

router = APIRouter(prefix="/eval", tags=["eval"])


@router.post("/run")
def run_eval() -> dict[str, object]:
    """Run first-stage proxy evaluation over sample questions."""

    return run_sample_evaluation()
