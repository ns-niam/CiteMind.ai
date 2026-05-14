from __future__ import annotations

from statistics import mean, pstdev
from typing import Any, Dict, List


FEATURE_COLUMNS = [
    "top_score",
    "avg_score",
    "min_score",
    "max_score",
    "score_std",
    "citation_count",
    "context_chars",
    "question_len",
    "answer_len",
    "response_time",
]


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        if value is None:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def build_feature_row(
    question: str,
    answer: str,
    citations: List[Dict[str, Any]],
    response_time: float | None = None,
    extra: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Convert one RAG result into ML features.
    Safe to call even if citations are empty.
    """
    extra = extra or {}

    scores = [_safe_float(c.get("score", 0.0)) for c in citations]
    if scores:
        top_score = max(scores)
        avg_score = mean(scores)
        min_score = min(scores)
        max_score = max(scores)
        score_std = pstdev(scores) if len(scores) > 1 else 0.0
    else:
        top_score = 0.0
        avg_score = 0.0
        min_score = 0.0
        max_score = 0.0
        score_std = 0.0

    context_chars = sum(len(str(c.get("text", ""))) for c in citations)

    row = {
        "top_score": round(top_score, 6),
        "avg_score": round(avg_score, 6),
        "min_score": round(min_score, 6),
        "max_score": round(max_score, 6),
        "score_std": round(score_std, 6),
        "citation_count": len(citations),
        "context_chars": context_chars,
        "question_len": len((question or "").split()),
        "answer_len": len((answer or "").split()),
        "response_time": _safe_float(response_time, 0.0),
    }

    for key, value in extra.items():
        row[key] = value

    return row