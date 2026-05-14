"""
CiteMind AI - RAG Engine
End-to-end pipeline: Query → Retrieve → Generate → Cite.
"""
from __future__ import annotations

import time
from typing import Dict, List

from src.generation.citations import CitationTracker
from src.generation.llm import get_llm
from src.generation.prompts import (
    NO_CONTEXT_RESPONSE,
    SYSTEM_PROMPT,
    build_prompt,
)
from src.ml.runtime import ConfidenceRuntime
from src.retrieval.retriever import Retriever
from src.retrieval.vectorstore import VectorStore


class RAGEngine:
    """The full Retrieval-Augmented Generation pipeline."""

    # Confidence thresholds based on retrieval score
    LOW_CONFIDENCE_THRESHOLD = 0.30
    MEDIUM_CONFIDENCE_THRESHOLD = 0.50

    def __init__(self, llm_provider: str = None, vectorstore: VectorStore = None):
        self.vs = vectorstore or VectorStore()
        self.retriever = Retriever(self.vs)
        self.llm = get_llm(llm_provider)
        self.provider = self.llm.provider

        # ML confidence runtime
        self.confidence_runtime = ConfidenceRuntime()

    def ask(
        self,
        question: str,
        top_k: int = None,
        use_mmr: bool = True,
        verbose: bool = False,
    ) -> Dict:
        """
        Ask a question and return answer + citations + metadata.
        """

        result = {
            "question": question,
            "provider": self.provider,
            "answer": "",
            "citations": [],
            "confidence": "none",
            "confidence_source": "heuristic",
            "confidence_probabilities": {},
            "confidence_error": "",
            "retrieval_time": 0,
            "llm_time": 0,
            "total_time": 0,
        }

        t_start = time.time()

        # =========================================================
        # Step 1: Retrieve relevant chunks
        # =========================================================
        t0 = time.time()

        chunks = self.retriever.retrieve(
            question,
            top_k=top_k,
            use_mmr=use_mmr,
        )

        result["retrieval_time"] = round(time.time() - t0, 3)

        if not chunks:
            result["answer"] = NO_CONTEXT_RESPONSE
            result["confidence"] = "none"
            result["confidence_source"] = "no_context"
            result["total_time"] = round(time.time() - t_start, 3)
            return result

        # =========================================================
        # Step 2: Heuristic confidence from retrieval score
        # =========================================================
        top_score = chunks[0].get("score", 0)

        if top_score < self.LOW_CONFIDENCE_THRESHOLD:
            heuristic_confidence = "low"

        elif top_score < self.MEDIUM_CONFIDENCE_THRESHOLD:
            heuristic_confidence = "medium"

        else:
            heuristic_confidence = "high"

        result["confidence"] = heuristic_confidence
        result["confidence_source"] = "heuristic"

        # =========================================================
        # Step 3: Format citations/context
        # =========================================================
        context, citations = CitationTracker.format_context(chunks)

        result["citations"] = citations

        if verbose:
            print(
                f"\n🔍 Retrieved {len(chunks)} chunks "
                f"(top score: {top_score:.3f})"
            )
            print(f"📊 Heuristic confidence: {heuristic_confidence}")

        # =========================================================
        # Step 4: Build prompt and call LLM
        # =========================================================
        user_prompt = build_prompt(context, question)

        if heuristic_confidence == "low":
            user_prompt = (
                "NOTE: Retrieval scores are low. "
                "Be extra cautious — if the context "
                "doesn't really answer the question, "
                "say so explicitly.\n\n"
                + user_prompt
            )

        t0 = time.time()

        try:
            answer = self.llm.ask(
                user_prompt,
                system_prompt=SYSTEM_PROMPT,
            )

            result["answer"] = answer

        except Exception as e:
            result["answer"] = f"❌ LLM error: {e}"

        result["llm_time"] = round(time.time() - t0, 3)

        # =========================================================
        # Step 5: ML confidence prediction
        # =========================================================
        try:
            ml_prediction = (
                self.confidence_runtime.predict_from_rag_result(result)
            )

            if ml_prediction.get("model_ready", False):

                ml_label = ml_prediction["label"]

                # Hybrid confidence boosting
                if top_score >= 0.65:
                    final_confidence = "high"

                elif top_score >= 0.45 and ml_label == "low":
                    final_confidence = "medium"

                else:
                    final_confidence = ml_label

                result["confidence"] = final_confidence
                result["confidence_source"] = "hybrid_ml"

                result["confidence_probabilities"] = (
                    ml_prediction["probabilities"]
                )

            else:
                result["confidence"] = heuristic_confidence
                result["confidence_source"] = "heuristic_fallback"

        except Exception as e:
            result["confidence_error"] = str(e)
            result["confidence"] = heuristic_confidence
            result["confidence_source"] = "heuristic_fallback"

        # =========================================================
        # Final timing
        # =========================================================
        result["total_time"] = round(time.time() - t_start, 3)

        return result

    def ask_both_llms(self, question: str, **kwargs) -> Dict[str, Dict]:
        """Ask the same question with both Groq and Gemini."""

        results = {}

        for provider in ["groq", "gemini"]:
            engine = RAGEngine(
                llm_provider=provider,
                vectorstore=self.vs,
            )

            results[provider] = engine.ask(question, **kwargs)

        return results