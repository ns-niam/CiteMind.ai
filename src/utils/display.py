"""
CiteMind AI - Display Helpers
Pretty terminal output for RAG results.
"""
from typing import Dict


def print_result(result: Dict):
    """Pretty-print a RAG result to the terminal."""
    print("\n" + "=" * 70)
    print(f"❓ Question: {result['question']}")
    print("=" * 70)

    # Confidence badge
    badges = {
        "high": "🟢 HIGH",
        "medium": "🟡 MEDIUM",
        "low": "🔴 LOW",
        "none": "⚫ NONE",
    }
    print(f"\n📊 Confidence: {badges.get(result['confidence'], '?')}")
    print(f"🤖 LLM: {result['provider'].upper()}")
    print(
        f"⏱️  Timing → Retrieval: {result['retrieval_time']}s | "
        f"LLM: {result['llm_time']}s | Total: {result['total_time']}s"
    )

    print("\n💬 ANSWER:")
    print("-" * 70)
    print(result["answer"])
    print("-" * 70)

    if result["citations"]:
        print(f"\n📚 SOURCES ({len(result['citations'])}):")
        for c in result["citations"]:
            print(f"  [{c['id']}] {c['source']}, page {c['page']} "
                  f"(relevance: {c['score']})")
            preview = c["text"][:140].replace("\n", " ")
            print(f"      → \"{preview}...\"\n")