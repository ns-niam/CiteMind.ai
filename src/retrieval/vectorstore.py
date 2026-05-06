"""
CiteMind AI - Vector Store
ChromaDB wrapper for storing and searching document chunks.
"""
from typing import List, Dict
import chromadb
from chromadb.config import Settings

from src.data.loader import LoadedChunk
from src.embeddings.embedder import Embedder
from src.utils.config import config


class VectorStore:
    """Persistent vector store using ChromaDB."""

    def __init__(self, collection_name: str = None, persist_dir: str = None):
        self.collection_name = collection_name or config.COLLECTION_NAME
        self.persist_dir = persist_dir or config.CHROMA_PERSIST_DIR

        self.client = chromadb.PersistentClient(
            path=self.persist_dir,
            settings=Settings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        self.embedder = Embedder()

    def add_chunks(self, chunks: List[LoadedChunk], batch_size: int = 64):
        """Embed and store chunks with metadata."""
        if not chunks:
            return

        texts = [c.text for c in chunks]
        metadatas = [
            {"source": c.source, "page": c.page, "chunk_idx": i}
            for i, c in enumerate(chunks)
        ]
        ids = [f"{c.source}_p{c.page}_c{i}" for i, c in enumerate(chunks)]

        # Batch embed + add
        for start in range(0, len(texts), batch_size):
            end = start + batch_size
            batch_texts = texts[start:end]
            vectors = self.embedder.encode(batch_texts).tolist()
            self.collection.add(
                ids=ids[start:end],
                embeddings=vectors,
                documents=batch_texts,
                metadatas=metadatas[start:end],
            )

    def search(self, query: str, top_k: int = None) -> List[Dict]:
        """Search top-k most similar chunks."""
        top_k = top_k or config.TOP_K
        query_vec = self.embedder.encode_one(query).tolist()

        results = self.collection.query(
            query_embeddings=[query_vec],
            n_results=top_k,
        )

        hits = []
        for i in range(len(results["ids"][0])):
            hits.append({
                "id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
                "score": 1.0 - results["distances"][0][i],  # cosine similarity
            })
        return hits

    def count(self) -> int:
        return self.collection.count()

    def reset(self):
        """Delete all data in the collection (use carefully)."""
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )