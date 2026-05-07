"""
CiteMind AI - Interactive CLI Chat
Talk to your documents from the terminal.
Run: python chat.py
"""
from src.retrieval.vectorstore import VectorStore
from src.data.ingest import ingest_directory
from src.generation.rag_engine import RAGEngine
from src.utils.display import print_result


def main():
    print("=" * 70)
    print("🧠 CiteMind AI - Interactive Chat")
    print("=" * 70)

    # Setup
    vs = VectorStore()
    if vs.count() == 0:
        print("\n📦 No documents indexed yet.")
        ingest_directory("data/raw", reset=False)

    print(f"\n✅ Ready! {vs.count()} chunks indexed.")
    print("\nCommands:")
    print("  • Type your question and press Enter")
    print("  • Type 'switch' to toggle between Groq/Gemini")
    print("  • Type 'quit' or 'exit' to leave")
    print("=" * 70)

    provider = "groq"
    engine = RAGEngine(llm_provider=provider)

    while True:
        try:
            q = input(f"\n[{provider.upper()}] 💬 You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Goodbye!")
            break

        if not q:
            continue
        if q.lower() in {"quit", "exit", "q"}:
            print("👋 Goodbye!")
            break
        if q.lower() == "switch":
            provider = "gemini" if provider == "groq" else "groq"
            engine = RAGEngine(llm_provider=provider)
            print(f"🔄 Switched to {provider.upper()}")
            continue

        result = engine.ask(q)
        print_result(result)


if __name__ == "__main__":
    main()