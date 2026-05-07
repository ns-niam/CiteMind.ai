"""
CiteMind AI - RAG Engine
End-to-end pipeline: Query → Retrieve → Generate → Cite.
"""
import time
from typing import Dict, List

from src.retrieval.retriever import Retriever
from src.retrieval.vectorstore import VectorStore
from src.generation.llm import get_llm
from src.generation.citations import CitationTracker
from src.generation.prompts import SYSTEM_PROMPT, build_prompt, NO_CONTEXT_RESPONSE
from src.utils.config import config


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

    def ask(
        self,
        question: str,
        top_k: int = None,
        use_mmr: bool = True,
        verbose: bool = False,
    ) -> Dict:
        """
        Ask a question and return answer + citations + metadata.

        Returns:
            {
                "answer": str,
                "citations": List[Dict],
                "confidence": str,  # "high" / "medium" / "low" / "none"
                "retrieval_time": float,
                "llm_time": float,
                "total_time": float,
                "provider": str,
            }
        """
        result = {
            "question": question,
            "provider": self.provider,
            "answer": "",
            "citations": [],
            "confidence": "none",
            "retrieval_time": 0,
            "llm_time": 0,
            "total_time": 0,
        }

        t_start = time.time()

        # Step 1: Retrieve
        t0 = time.time()
        chunks = self.retriever.retrieve(question, top_k=top_k, use_mmr=use_mmr)
        result["retrieval_time"] = round(time.time() - t0, 3)

        if not chunks:
            result["answer"] = NO_CONTEXT_RESPONSE
            result["confidence"] = "none"
            result["total_time"] = round(time.time() - t_start, 3)
            return result

        # Step 2: Confidence check
        top_score = chunks[0].get("score", 0)
        if top_score < self.LOW_CONFIDENCE_THRESHOLD:
            confidence = "low"
        elif top_score < self.MEDIUM_CONFIDENCE_THRESHOLD:
            confidence = "medium"
        else:
            confidence = "high"
        result["confidence"] = confidence

        # Step 3: Format context with citations
        context, citations = CitationTracker.format_context(chunks)
        result["citations"] = citations

        if verbose:
            print(f"\n🔍 Retrieved {len(chunks)} chunks (top score: {top_score:.3f})")
            print(f"📊 Confidence: {confidence}")

        # Step 4: Build prompt and call LLM
        user_prompt = build_prompt(context, question)
        if confidence == "low":
            user_prompt = (
                "NOTE: Retrieval scores are low. Be extra cautious — if the context "
                "doesn't really answer the question, say so explicitly.\n\n" + user_prompt
            )

        t0 = time.time()
        try:
            answer = self.llm.ask(user_prompt, system_prompt=SYSTEM_PROMPT)
            result["answer"] = answer
        except Exception as e:
            result["answer"] = f"❌ LLM error: {e}"
        result["llm_time"] = round(time.time() - t0, 3)

        result["total_time"] = round(time.time() - t_start, 3)
        return result

    def ask_both_llms(self, question: str, **kwargs) -> Dict[str, Dict]:
        """Ask the same question with both Groq and Gemini for comparison."""
        results = {}
        for provider in ["groq", "gemini"]:
            engine = RAGEngine(llm_provider=provider, vectorstore=self.vs)
            results[provider] = engine.ask(question, **kwargs)
        return results