"""
CiteMind AI - Embedding Module
Wraps sentence-transformers for generating dense vectors.
"""
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

from src.utils.config import config


class Embedder:
    """Generates dense vector embeddings for text."""

    _instance = None  # Singleton — load model only once

    def __new__(cls, model_name: str = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init(model_name)
        return cls._instance

    def _init(self, model_name: str = None):
        self.model_name = model_name or config.EMBEDDING_MODEL
        print(f"🧮 Loading embedding model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        self.dim = self.model.get_sentence_embedding_dimension()
        print(f"✅ Embedding model loaded (dim={self.dim})")

    def encode(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """Encode list of texts into vectors."""
        return self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True,  # for cosine similarity
        )

    def encode_one(self, text: str) -> np.ndarray:
        """Encode single text."""
        return self.encode([text])[0]