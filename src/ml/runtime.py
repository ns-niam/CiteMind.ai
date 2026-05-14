from __future__ import annotations

from typing import Dict, Any

from src.ml.confidence_model import ConfidenceModel
from src.ml.feature_builder import build_feature_row


class ConfidenceRuntime:
    """
    Safe runtime wrapper around the trained confidence model.
    Falls back gracefully if model unavailable.
    """

    def __init__(self):
        self.model = ConfidenceModel()

    def predict_from_rag_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict confidence using a trained ML model.
        Returns:
        {
            "label": "high" | "medium" | "low",
            "probabilities": {...},
            "model_ready": bool
        }
        """

        features = build_feature_row(
            question=result.get("question", ""),
            answer=result.get("answer", ""),
            citations=result.get("citations", []),
            response_time=result.get("total_time", 0.0),
        )

        label = self.model.predict(features)
        probs = self.model.predict_proba(features)

        return {
            "label": label,
            "probabilities": probs,
            "model_ready": self.model.is_ready(),
        }