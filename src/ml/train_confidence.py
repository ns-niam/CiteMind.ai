from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.ml.feature_builder import FEATURE_COLUMNS


def load_dataset(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    required = {"label", *FEATURE_COLUMNS}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Dataset missing columns: {sorted(missing)}")

    df = df.dropna(subset=["label"]).copy()
    df["label"] = df["label"].astype(str).str.lower().str.strip()

    if df["label"].nunique() < 2:
        raise ValueError(
            "Dataset must contain at least 2 labels. "
            "Rebuild the dataset with balanced labels first."
        )

    return df


def train_model(df: pd.DataFrame):
    X = df[FEATURE_COLUMNS].copy()
    y = df["label"].copy()

    class_counts = y.value_counts()
    can_stratify = len(df) >= 15 and len(class_counts) >= 2 and class_counts.min() >= 2

    if can_stratify:
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.25,
            random_state=42,
            stratify=y,
        )
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.25,
            random_state=42,
            shuffle=True,
        )

    model = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            (
                "clf",
                RandomForestClassifier(
                    n_estimators=300,
                    random_state=42,
                    class_weight="balanced",
                ),
            ),
        ]
    )

    model.fit(X_train, y_train)

    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)

    label_order = [lbl for lbl in ["low", "medium", "high"] if lbl in y.unique()]

    metrics = {
        "train_accuracy": round(accuracy_score(y_train, train_pred), 4),
        "test_accuracy": round(accuracy_score(y_test, test_pred), 4),
        "test_f1_macro": round(f1_score(y_test, test_pred, average="macro"), 4),
    }

    report = classification_report(
        y_test,
        test_pred,
        labels=label_order if label_order else None,
        zero_division=0,
    )

    cm = confusion_matrix(
        y_test,
        test_pred,
        labels=label_order if label_order else sorted(y.unique()),
    )

    return model, metrics, report, cm, sorted(y.unique())


def main():
    parser = argparse.ArgumentParser(description="Train confidence classifier")
    parser.add_argument(
        "--data",
        default="data/ml/confidence_dataset.csv",
        help="Training CSV file",
    )
    parser.add_argument(
        "--out",
        default="models/confidence_model.joblib",
        help="Output model path",
    )
    parser.add_argument(
        "--summary-out",
        default="models/confidence_training_summary.json",
        help="Output summary JSON path",
    )
    parser.add_argument(
        "--experiment",
        default="CiteMind-Confidence-Model",
        help="MLflow experiment name",
    )
    args = parser.parse_args()

    df = load_dataset(args.data)
    print(f"✅ Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")
    print("\nLabel distribution:")
    print(df["label"].value_counts().to_string())

    model, metrics, report, cm, classes = train_model(df)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(
        {
            "model": model,
            "feature_columns": FEATURE_COLUMNS,
            "classes": classes,
        },
        out_path,
    )

    summary = {
        "dataset_rows": int(df.shape[0]),
        "dataset_columns": int(df.shape[1]),
        "feature_columns": FEATURE_COLUMNS,
        "metrics": metrics,
        "classification_report": report,
        "confusion_matrix": cm.tolist(),
        "classes": classes,
    }

    summary_path = Path(args.summary_out)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # ---------------- MLflow Logging ----------------
    mlflow.set_tracking_uri("file:./mlruns")
    mlflow.set_experiment(args.experiment)

    with mlflow.start_run():
        mlflow.log_param("model_type", "RandomForestClassifier")
        mlflow.log_param("n_estimators", 300)
        mlflow.log_param("random_state", 42)
        mlflow.log_param("class_weight", "balanced")
        mlflow.log_param("dataset_rows", int(df.shape[0]))
        mlflow.log_param("dataset_columns", int(df.shape[1]))
        mlflow.log_param("feature_count", len(FEATURE_COLUMNS))
        mlflow.log_param("train_test_split", "0.75/0.25")

        for k, v in metrics.items():
            mlflow.log_metric(k, v)

        mlflow.log_text(report, "classification_report.txt")
        mlflow.log_text(json.dumps(summary, indent=2), "training_summary.json")
        mlflow.log_text(
            "\n".join(["\t".join(map(str, row)) for row in cm]),
            "confusion_matrix.txt",
        )

        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="confidence_model",
        )

    print("\n✅ Model saved to:", out_path)
    print("✅ Summary saved to:", summary_path)

    print("\nMetrics:")
    for k, v in metrics.items():
        print(f"  {k}: {v}")

    print("\nClassification report:")
    print(report)

    print("\nConfusion matrix:")
    print(cm)


if __name__ == "__main__":
    main()