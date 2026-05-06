# 🧠 CiteMind AI

> An intelligent research assistant powered by Ret
rieval-Augmented Generation (RAG) that provides accurate, context-aware answers with verifiable source citations from research documents.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)

---

## 📌 Problem Statement

Researchers, students, and academics spend countless hours sifting through dozens of research papers to find specific information. Traditional keyword-based search returns documents — not answers. When LLMs are used directly, they hallucinate facts and cannot cite sources, making them unreliable for academic work.

**CiteMind AI solves this** by combining the reasoning power of Large Language Models with a verifiable retrieval system that grounds every answer in actual research documents and provides precise citations.

---

## ✨ Key Features

- 📄 **Multi-format Support** — Upload PDFs, DOCX, and TXT research papers
- 🔍 **Semantic Search** — Find relevant content by meaning, not just keywords
- 💬 **Natural Q&A** — Ask questions in plain English
- 📚 **Source Citations** — Every answer includes page numbers and document references
- ⚡ **Dual LLM** — Groq (fast) + Gemini (accurate) for better answers
- 📊 **RAG Evaluation** — Built-in metrics (Faithfulness, Relevancy, Precision)

---

## 🏗️ System Architecture

User Query → Embedding → Vector Search → Top-K Retrieval ↓ Context + Query → LLM → Answer + Citations


*(Detailed architecture diagram in `/docs`)*

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| Framework | LangChain |
| Embeddings | sentence-transformers |
| Vector DB | ChromaDB |
| LLM | Groq (Llama 3.1) + Google Gemini |
| Frontend | Streamlit |
| Evaluation | RAGAS |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Groq API key ([get free](https://console.groq.com))
- Google Gemini API key ([get free](https://aistudio.google.com/apikey))

### Installation

```bash
# Clone the repository
git clone https://github.com/ns-niam/CiteMind.ai.git
cd CiteMind.ai

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your API keys
Run the App
streamlit run app.py
📁 Project Structure
CiteMind.ai/
├── src/
│   ├── data/          # Document loaders & preprocessing
│   ├── embeddings/    # Embedding model wrappers
│   ├── retrieval/     # Vector search logic
│   ├── generation/    # LLM integration
│   ├── evaluation/    # RAG metrics
│   └── utils/         # Helpers
├── notebooks/         # Jupyter experiments
├── data/              # Raw & processed documents
├── tests/             # Unit tests
├── docs/              # Architecture & reports
├── app.py             # Streamlit frontend
└── requirements.txt
📅 Development Roadmap
 Day 1: Project setup
 Day 2-3: Problem statement & architecture
 Day 4-6: Data pipeline
 Day 7-11: Core RAG engine
 Day 12-14: Evaluation & metrics
 Day 15-17: Frontend & integration
 Day 18-20: Documentation & defense
👤 Author
ns-niam

GitHub: @ns-niam
📄 License
not for use without taking permission 