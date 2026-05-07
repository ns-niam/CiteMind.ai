"""
CiteMind AI - Ingestion Pipeline
One-shot: load directory → chunk → embed → store.
"""
from src.data.loader import DocumentLoader
from src.data.chunker import Chunker
from src.retrieval.vectorstore import VectorStore


def ingest_directory(dir_path: str, reset: bool = False) -> int:
    """Ingest all documents from a directory. Returns number of chunks indexed."""
    print(f"📥 Loading documents from {dir_path}/")
    loader = DocumentLoader()
    docs = loader.load_directory(dir_path)
    if not docs:
        print("⚠️  No documents found.")
        return 0

    print(f"\n✂️  Chunking {len(docs)} pages/sections")
    chunker = Chunker()
    chunks = chunker.split(docs)
    print(f"   → {len(chunks)} chunks")

    print(f"\n💾 Indexing into vector store")
    vs = VectorStore()
    if reset:
        print("   ⚠️  Resetting existing index...")
        vs.reset()
    vs.add_chunks(chunks)
    print(f"   ✅ Indexed {vs.count()} total chunks\n")
    return vs.count()


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "data/raw"
    reset = "--reset" in sys.argv
    ingest_directory(path, reset=reset)