"""
Test the full retrieval pipeline:
Load PDF → Chunk → Index → Search → Format Citations
Run: python -m tests.test_retrieval
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.loader import DocumentLoader
from src.data.chunker import Chunker
from src.retrieval.vectorstore import VectorStore
from src.retrieval.retriever import Retriever
from src.generation.citations import CitationTracker


def main():
    print("=" * 60)
    print("🧠 CiteMind AI - Retrieval Pipeline Test")
    print("=" * 60)

    # Step 1: Build the index (ingest documents)
    print("\n📥 Step 1: Loading + Chunking documents")
    loader = DocumentLoader()
    chunker = Chunker()
    docs = loader.load_directory("data/raw")
    chunks = chunker.split(docs)
    print(f"   → {len(chunks)} chunks ready")

    print("\n💾 Step 2: Indexing into ChromaDB")
    vs = VectorStore()
    vs.reset()  # fresh start for testing
    vs.add_chunks(chunks)
    print(f"   → Vector store has {vs.count()} chunks indexed")

    # Step 3: Run several test queries
    queries = [
        "What is the attention mechanism?",
        "How does multi-head attention work?",
        "What are the advantages of transformers over RNNs?",
        "What dataset was used for training?",
    ]

    retriever = Retriever(vs)

    for q in queries:
        print("\n" + "=" * 60)
        print(f"🔍 Query: {q}")
        print("=" * 60)

        results = retriever.retrieve(q, top_k=3, use_mmr=True)
        context, citations = CitationTracker.format_context(results)

        print(f"\nTop {len(results)} chunks retrieved:\n")
        for c in citations:
            print(f"  [{c['id']}] {c['source']}, p.{c['page']} "
                  f"(score: {c['score']})")
            print(f"      → \"{c['text'][:120]}...\"\n")

    print("\n" + "=" * 60)
    print("🎉 Retrieval pipeline working!")
    print("=" * 60)


if __name__ == "__main__":
    main()