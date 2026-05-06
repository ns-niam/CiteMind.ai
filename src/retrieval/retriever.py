"""
CiteMind AI - Retriever
High-level retrieval with optional MMR (diversity re-ranking).
"""
from typing import List, Dict
import numpy as np

from src.retrieval.vectorstore import VectorStore
from src.embeddings.embedder import Embedder
from src.utils.config import config


class Retriever:
    """Retrieval with similarity search + optional MMR."""

    def __init__(self, vectorstore: VectorStore = None):
        self.vs = vectorstore or VectorStore()
        self.embedder = Embedder()

    def retrieve(
        self,
        query: str,
        top_k: int = None,
        use_mmr: bool = True,
        mmr_lambda: float = 0.5,
        fetch_k: int = 20,
    ) -> List[Dict]:
        """Retrieve relevant chunks for a query."""
        top_k = top_k or config.TOP_K

        if not use_mmr:
            return self.vs.search(query, top_k=top_k)

        # MMR: fetch more candidates, then re-rank for diversity
        candidates = self.vs.search(query, top_k=fetch_k)
        if len(candidates) <= top_k:
            return candidates

        return self._mmr_rerank(query, candidates, top_k, mmr_lambda)

    def _mmr_rerank(
        self, query: str, candidates: List[Dict], top_k: int, lambda_param: float
    ) -> List[Dict]:
        """Maximal Marginal Relevance — balance relevance and diversity."""
        query_vec = self.embedder.encode_one(query)
        cand_vecs = self.embedder.encode([c["text"] for c in candidates])

        selected = []
        selected_idx = []
        remaining = list(range(len(candidates)))

        # Pick first: highest similarity to query
        sims_to_query = cand_vecs @ query_vec
        first = int(np.argmax(sims_to_query))
        selected.append(candidates[first])
        selected_idx.append(first)
        remaining.remove(first)

        # Iteratively pick: balance relevance vs diversity
        while len(selected) < top_k and remaining:
            scores = []
            for idx in remaining:
                relevance = sims_to_query[idx]
                diversity = max(
                    cand_vecs[idx] @ cand_vecs[s_idx] for s_idx in selected_idx
                )
                mmr_score = lambda_param * relevance - (1 - lambda_param) * diversity
                scores.append((idx, mmr_score))

            best_idx, _ = max(scores, key=lambda x: x[1])
            selected.append(candidates[best_idx])
            selected_idx.append(best_idx)
            remaining.remove(best_idx)

        return selected