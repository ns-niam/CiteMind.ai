"""
CiteMind AI - RAG Evaluation
Custom lightweight metrics + RAGAS-style evaluation.
"""
import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer

from src.embeddings.embedder import Embedder


class RAGEvaluator:
    """Lightweight reference-based RAG evaluation."""

    def __init__(self):
        self.embedder = Embedder()

    @staticmethod
    def _cosine(a: np.ndarray, b: np.ndarray) -> float:
        denom = (np.linalg.norm(a) * np.linalg.norm(b)) + 1e-9
        return float(np.dot(a, b) / denom)

    def answer_relevancy(self, question: str, answer: str) -> float:
        """How well does the answer address the question? (semantic similarity)"""
        q_vec = self.embedder.encode_one(question)
        a_vec = self.embedder.encode_one(answer)
        return round(self._cosine(q_vec, a_vec), 3)

    def answer_correctness(self, answer: str, ground_truth: str) -> float:
        """Semantic similarity between generated answer and ground truth."""
        a_vec = self.embedder.encode_one(answer)
        g_vec = self.embedder.encode_one(ground_truth)
        return round(self._cosine(a_vec, g_vec), 3)

    def context_precision(self, question: str, contexts: List[str]) -> float:
        """Avg semantic similarity of retrieved chunks to question."""
        if not contexts:
            return 0.0
        q_vec = self.embedder.encode_one(question)
        c_vecs = self.embedder.encode(contexts)
        sims = [self._cosine(q_vec, cv) for cv in c_vecs]
        return round(float(np.mean(sims)), 3)

    def faithfulness(self, answer: str, contexts: List[str]) -> float:
        """How faithful is the answer to the retrieved context?"""
        if not contexts:
            return 0.0
        a_vec = self.embedder.encode_one(answer)
        c_vecs = self.embedder.encode(contexts)
        sims = [self._cosine(a_vec, cv) for cv in c_vecs]
        return round(float(np.max(sims)), 3)

    def evaluate_one(
        self, question: str, answer: str, contexts: List[str], ground_truth: str
    ) -> Dict[str, float]:
        """Run all metrics on a single QA example."""
        return {
            "answer_relevancy": self.answer_relevancy(question, answer),
            "answer_correctness": self.answer_correctness(answer, ground_truth),
            "context_precision": self.context_precision(question, contexts),
            "faithfulness": self.faithfulness(answer, contexts),
        }

    def evaluate_batch(self, results: List[Dict]) -> Dict:
        """Aggregate results from multiple queries."""
        if not results:
            return {}
        keys = ["answer_relevancy", "answer_correctness",
                "context_precision", "faithfulness"]
        agg = {k: round(np.mean([r[k] for r in results]), 3) for k in keys}
        agg["n_samples"] = len(results)
        return agg