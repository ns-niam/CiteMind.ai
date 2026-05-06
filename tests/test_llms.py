"""
Test both Groq and Gemini LLMs.
Run: python -m tests.test_llms
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.config import config
from src.generation.llm import get_llm


def main():
    print("=" * 60)
    print("🧠 CiteMind AI - LLM Test")
    print("=" * 60)

    # Validate keys
    missing = config.validate()
    if missing:
        print(f"\n❌ Missing API keys: {', '.join(missing)}")
        print("Please set them in your .env file.")
        return

    print("\n✅ API keys loaded\n")

    test_question = (
        "What is Retrieval-Augmented Generation (RAG)? "
        "Answer in 2-3 sentences."
    )

    # Test Groq
    print("-" * 60)
    print("🚀 Testing Groq (Llama 3.3 70B)")
    print("-" * 60)
    try:
        groq_llm = get_llm("groq")
        answer = groq_llm.ask(test_question)
        print(f"\n{answer}\n")
        print("✅ Groq working!\n")
    except Exception as e:
        print(f"❌ Groq error: {e}\n")

    # Test Gemini
    print("-" * 60)
    print("✨ Testing Gemini (2.0 Flash)")
    print("-" * 60)
    try:
        gemini_llm = get_llm("gemini")
        answer = gemini_llm.ask(test_question)
        print(f"\n{answer}\n")
        print("✅ Gemini working!\n")
    except Exception as e:
        print(f"❌ Gemini error: {e}\n")

    print("=" * 60)
    print("🎉 LLM tests complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()