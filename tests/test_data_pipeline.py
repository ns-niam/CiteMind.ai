"""
Test the full data pipeline: Load → Chunk → Embed
Run: python -m tests.test_data_pipeline
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.loader import DocumentLoader
from src.data.chunker import Chunker
from src.embeddings.embedder import Embedder


def main():
    print("=" * 60)
    print("🧠 CiteMind AI - Data Pipeline Test")
    print("=" * 60)

    # Step 1: Load
    print("\n📥 Step 1: Loading documents from data/raw/")
    loader = DocumentLoader()
    docs = loader.load_directory("data/raw")
    print(f"   → Loaded {len(docs)} pages/sections")

    if not docs:
        print("❌ No documents found! Add files to data/raw/")
        return

    # Show sample
    print(f"\n   Sample (first page, first 200 chars):")
    print(f"   '{docs[0].text[:200]}...'")
    print(f"   Source: {docs[0].source}, Page: {docs[0].page}")

    # Step 2: Chunk
    print("\n✂️  Step 2: Chunking documents")
    chunker = Chunker()
    chunks = chunker.split(docs)
    print(f"   → {len(docs)} pages → {len(chunks)} chunks")
    print(f"   Avg chunk length: {sum(len(c.text) for c in chunks) // len(chunks)} chars")

    # Step 3: Embed
    print("\n🧮 Step 3: Generating embeddings")
    embedder = Embedder()
    texts = [c.text for c in chunks[:10]]  # first 10 for speed
    vectors = embedder.encode(texts)
    print(f"   → Encoded {len(vectors)} chunks")
    print(f"   Vector shape: {vectors.shape}")
    print(f"   Sample vector (first 5 dims): {vectors[0][:5]}")

    print("\n" + "=" * 60)
    print("🎉 Data pipeline working end-to-end!")
    print("=" * 60)


if __name__ == "__main__":
    main()