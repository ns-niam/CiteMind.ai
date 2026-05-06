"""
CiteMind AI - Configuration Module
Loads environment variables and provides settings.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    # LLM Settings
    DEFAULT_LLM = os.getenv("DEFAULT_LLM", "groq")
    GROQ_MODEL = "llama-3.3-70b-versatile"
    GEMINI_MODEL = "gemini-2.5-flash"

    # Embedding
    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )

    # Vector DB
    CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "citemind_docs")

    # Chunking
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))

    # Retrieval
    TOP_K = int(os.getenv("TOP_K", 5))

    @classmethod
    def validate(cls):
        """Check that required keys are set."""
        missing = []
        if not cls.GROQ_API_KEY or cls.GROQ_API_KEY.startswith("your_"):
            missing.append("GROQ_API_KEY")
        if not cls.GOOGLE_API_KEY or cls.GOOGLE_API_KEY.startswith("your_"):
            missing.append("GOOGLE_API_KEY")
        return missing


config = Config()