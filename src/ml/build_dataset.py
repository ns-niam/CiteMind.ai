from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from src.ml.feature_builder import FEATURE_COLUMNS, build_feature_row


def build_dataset(eval_json_path: str, out_csv_path: str) -> pd.DataFrame:
    eval_path = Path(eval_json_path)
    out_path = Path(out_csv_path)

    if not eval_path.exists():
        raise FileNotFoundError(f"Evaluation file not found: {eval_path}")

    with eval_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    rows = []

    for provider, items in data.get("per_query", {}).items():
        for item in items:
            citations = item.get("citations", [])
            row = build_feature_row(
                question=item.get("question", ""),
                answer=item.get("answer", ""),
                citations=[
                    {
                        "score": c.get("score", 0.0),
                        "text": c.get("text", ""),
                    }
                    for c in citations
                ],
                response_time=item.get("total_time", 0.0),
                extra={
                    "provider": provider,
                    "answer_relevancy": item.get("answer_relevancy", 0.0),
                    "answer_correctness": item.get("answer_correctness", 0.0),
                    "context_precision": item.get("context_precision", 0.0),
                    "faithfulness": item.get("faithfulness", 0.0),
                },
            )
            rows.append(row)

    if not rows:
        raise ValueError("No rows found in evaluation file.")

    df = pd.DataFrame(rows)

    # Composite quality score for balanced bootstrapped labels
    df["quality_score"] = (
        0.35 * df["faithfulness"]
        + 0.25 * df["answer_relevancy"]
        + 0.20 * df["context_precision"]
        + 0.10 * df["answer_correctness"]
        + 0.10 * (df["citation_count"].clip(upper=5) / 5.0)
    )

    # Rank-based 3-way labeling to guarantee class diversity
    df = df.sort_values("quality_score").reset_index(drop=True)
    n = len(df)
    low_end = max(1, n // 3)
    high_start = max(low_end + 1, (2 * n) // 3)

    labels = []
    for idx in range(n):
        if idx < low_end:
            labels.append("low")
        elif idx < high_start:
            labels.append("medium")
        else:
            labels.append("high")

    df["label"] = labels

    ordered_cols = [
        "provider",
        *FEATURE_COLUMNS,
        "quality_score",
        "answer_relevancy",
        "answer_correctness",
        "context_precision",
        "faithfulness",
        "label",
    ]
    df = df[ordered_cols]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)

    print(f"✅ Dataset saved to: {out_path}")
    print("\nLabel distribution:")
    print(df["label"].value_counts().to_string())

    return df


def main():
    parser = argparse.ArgumentParser(description="Build confidence ML dataset from eval_results.json")
    parser.add_argument(
        "--eval-json",
        default="data/processed/eval_results.json",
        help="Path to eval_results.json",
    )
    parser.add_argument(
        "--out-csv",
        default="data/ml/confidence_dataset.csv",
        help="Output CSV path",
    )
    args = parser.parse_args()

    build_dataset(args.eval_json, args.out_csv)


if __name__ == "__main__":
    main()