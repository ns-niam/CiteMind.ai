"""
End-to-end RAG test: ingest → ask → answer with citations.
Run: python -m tests.test_rag
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.ingest import ingest_directory
from src.retrieval.vectorstore import VectorStore
from src.generation.rag_engine import RAGEngine
from src.utils.display import print_result


def main():
    print("=" * 70)
    print("🧠 CiteMind AI - END-TO-END RAG TEST")
    print("=" * 70)

    # Make sure index is built
    vs = VectorStore()
    if vs.count() == 0:
        print("\n📦 Index empty — running ingestion...")
        ingest_directory("data/raw", reset=False)
    else:
        print(f"\n✅ Using existing index ({vs.count()} chunks)")

    # Test queries
    queries = [
        "What is the attention mechanism in the Transformer?",
        "How does multi-head attention differ from single-head attention?",
        "What were the BLEU scores achieved on the English-to-German task?",
    ]

    # Test with Groq (faster)
    print("\n" + "🚀" * 35)
    print("Testing with GROQ")
    print("🚀" * 35)
    engine_groq = RAGEngine(llm_provider="groq")
    for q in queries:
        result = engine_groq.ask(q)
        print_result(result)

    # Compare both LLMs on one question
    print("\n" + "🆚" * 35)
    print("LLM COMPARISON: Groq vs Gemini")
    print("🆚" * 35)
    comparison_q = "Why is self-attention preferred over recurrent layers?"
    both = engine_groq.ask_both_llms(comparison_q)
    for provider, result in both.items():
        print_result(result)

    print("\n" + "=" * 70)
    print("🎉 RAG Engine fully operational!")
    print("=" * 70)


if __name__ == "__main__":
    main()