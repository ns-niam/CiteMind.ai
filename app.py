"""
CiteMind AI - Day 1 Setup Verification
"""
import sys
print("=" * 50)
print("🧠 CiteMind AI - Setup Verification")
print("=" * 50)

print(f"\n✅ Python version: {sys.version.split()[0]}")

# Test critical imports
packages = {
    "langchain": "LangChain",
    "chromadb": "ChromaDB",
    "sentence_transformers": "Sentence Transformers",
    "groq": "Groq",
    "google.generativeai": "Google Gemini",
    "streamlit": "Streamlit",
    "pdfplumber": "PDFPlumber",
}

print("\n📦 Checking installed packages:")
for pkg, name in packages.items():
    try:
        __import__(pkg)
        print(f"  ✅ {name}")
    except ImportError as e:
        print(f"  ❌ {name} - {e}")

print("\n🎉 Day 1 setup complete!")
print("Ready to build CiteMind AI 🚀")