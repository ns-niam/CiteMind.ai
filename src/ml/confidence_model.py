from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import joblib
import pandas as pd

from src.ml.feature_builder import FEATURE_COLUMNS, build_feature_row


class ConfidenceModel:
    """
    Loads a trained confidence classifier if available.
    Falls back to a safe heuristic if the model is missing.
    """

    def __init__(self, model_path: str = "models/confidence_model.joblib"):
        self.model_path = Path(model_path)
        self.model = None
        self.feature_columns = FEATURE_COLUMNS
        self.load()

    def load(self) -> None:
        if not self.model_path.exists():
            self.model = None
            return

        artifact = joblib.load(self.model_path)
        self.model = artifact.get("model", artifact)
        self.feature_columns = artifact.get("feature_columns", FEATURE_COLUMNS)

    def is_ready(self) -> bool:
        return self.model is not None

    def _to_frame(self, features: Dict[str, Any]) -> pd.DataFrame:
        row = {col: features.get(col, 0.0) for col in self.feature_columns}
        return pd.DataFrame([row])

    def predict(self, features: Dict[str, Any]) -> str:
        if not self.is_ready():
            return self._heuristic_predict(features)

        frame = self._to_frame(features)
        pred = self.model.predict(frame)[0]
        return str(pred)

    def predict_proba(self, features: Dict[str, Any]) -> Dict[str, float]:
        if not self.is_ready() or not hasattr(self.model, "predict_proba"):
            label = self._heuristic_predict(features)
            return {
                "low": 1.0 if label == "low" else 0.0,
                "medium": 1.0 if label == "medium" else 0.0,
                "high": 1.0 if label == "high" else 0.0,
            }

        frame = self._to_frame(features)
        probs = self.model.predict_proba(frame)[0]
        classes = list(self.model.classes_)
        return {str(cls): float(prob) for cls, prob in zip(classes, probs)}

    def predict_from_result(self, result: Dict[str, Any]) -> str:
        features = build_feature_row(
            question=result.get("question", ""),
            answer=result.get("answer", ""),
            citations=result.get("citations", []),
            response_time=result.get("total_time", 0.0),
        )
        return self.predict(features)

    @staticmethod
    def _heuristic_predict(features: Dict[str, Any]) -> str:
        top_score = float(features.get("top_score", 0.0))
        avg_score = float(features.get("avg_score", 0.0))
        citation_count = int(features.get("citation_count", 0))

        if top_score >= 0.70 and avg_score >= 0.55 and citation_count >= 2:
            return "high"
        if top_score >= 0.40 and citation_count >= 1:
            return "medium"
        return "low"