"""
CiteMind AI - Streamlit Web App
Crafted by Niam
Run: streamlit run app.py
"""
import os
from pathlib import Path

import streamlit as st

from src.data.loader import DocumentLoader
from src.data.chunker import Chunker
from src.retrieval.vectorstore import VectorStore
from src.generation.rag_engine import RAGEngine
from src.utils.config import config


# ─────────────────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CiteMind AI · by Niam",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────
# Custom CSS — Dark-mode friendly, glassmorphism, professional
# ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ===== Global Theme ===== */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }

    /* Keep menu visible for theme/recording, hide only footer */
    footer {visibility: hidden;}

    /* ===== Hero Header ===== */
    .hero {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.25) 0%, rgba(118, 75, 162, 0.25) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    .hero h1 {
        background: linear-gradient(90deg, #a8edea 0%, #fed6e3 50%, #ffd89b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        letter-spacing: -1px;
    }
    .hero p {
        color: rgba(255, 255, 255, 0.85);
        font-size: 1.05rem;
        margin-top: 0.5rem;
        margin-bottom: 0;
    }
    .hero .badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        color: #fed6e3;
        margin-top: 0.8rem;
        font-weight: 500;
    }

    /* ===== Stat Boxes (Dark mode fix!) ===== */
    .stat-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        backdrop-filter: blur(8px);
        transition: transform 0.2s;
    }
    .stat-box:hover {
        transform: translateY(-2px);
    }
    .stat-box h2 {
        color: #fed6e3 !important;
        font-size: 2rem !important;
        margin: 0 !important;
        font-weight: 800 !important;
    }
    .stat-box small {
        color: rgba(255, 255, 255, 0.7) !important;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ===== Source Cards (Dark mode) ===== */
    .source-card {
        background: rgba(255, 255, 255, 0.05);
        border-left: 3px solid #a8edea;
        border-radius: 8px;
        padding: 14px 18px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        transition: transform 0.2s, border-left-color 0.2s;
    }
    .source-card:hover {
        transform: translateX(4px);
        border-left-color: #fed6e3;
    }
    .source-card b {
        color: #a8edea;
    }
    .source-card small {
        color: rgba(255, 255, 255, 0.75);
        line-height: 1.5;
    }

    /* ===== Citation Badge ===== */
    .citation-badge {
        display: inline-block;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.78em;
        margin: 0 4px;
        font-weight: 600;
        box-shadow: 0 2px 6px rgba(102, 126, 234, 0.4);
    }

    /* ===== Confidence Indicators ===== */
    .confidence-high { color: #4ade80; font-weight: 700; }
    .confidence-medium { color: #fbbf24; font-weight: 700; }
    .confidence-low { color: #f87171; font-weight: 700; }
    .confidence-none { color: #94a3b8; font-weight: 700; }

    /* ===== Persistent Author Watermark ===== */
    .author-watermark {
        position: fixed;
        bottom: 18px;
        right: 22px;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.85) 0%, rgba(118, 75, 162, 0.85) 100%);
        backdrop-filter: blur(12px);
        color: white;
        padding: 8px 16px;
        border-radius: 24px;
        font-size: 0.82rem;
        font-weight: 600;
        z-index: 9999;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.2);
        letter-spacing: 0.3px;
    }
    .author-watermark::before {
        content: "✨ ";
    }

    /* ===== Sidebar Header ===== */
    .sidebar-section-title {
        color: #fed6e3 !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }

    /* ===== Chat message styling ===== */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1rem !important;
    }

    /* ===== Footer ===== */
    .custom-footer {
        text-align: center;
        padding: 1.5rem 0 4rem 0;
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.85rem;
    }
    .custom-footer b {
        background: linear-gradient(90deg, #a8edea 0%, #fed6e3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* ===== Welcome cards ===== */
    .welcome-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        height: 100%;
        backdrop-filter: blur(10px);
        transition: transform 0.2s;
    }
    .welcome-card:hover {
        transform: translateY(-4px);
        border-color: rgba(168, 237, 234, 0.4);
    }
    .welcome-card h4 {
        color: #a8edea !important;
        margin-top: 0 !important;
    }
    .welcome-card p {
        color: rgba(255, 255, 255, 0.75);
        margin-bottom: 0;
    }
</style>
""", unsafe_allow_html=True)



st.markdown(
    '<div class="author-watermark">Made by Niam</div>',
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────
# Session State
# ─────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = VectorStore()
if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = set()


# ─────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────
@st.cache_resource
def get_engine(provider: str):
    return RAGEngine(llm_provider=provider, vectorstore=st.session_state.vectorstore)


def ingest_uploaded_files(uploaded_files):
    if not uploaded_files:
        return 0

    upload_dir = Path("data/raw")
    upload_dir.mkdir(parents=True, exist_ok=True)

    new_chunks = 0
    loader = DocumentLoader()
    chunker = Chunker()

    for uploaded in uploaded_files:
        if uploaded.name in st.session_state.indexed_files:
            continue
        save_path = upload_dir / uploaded.name
        with open(save_path, "wb") as f:
            f.write(uploaded.getbuffer())
        try:
            docs = loader.load(str(save_path))
            chunks = chunker.split(docs)
            st.session_state.vectorstore.add_chunks(chunks)
            st.session_state.indexed_files.add(uploaded.name)
            new_chunks += len(chunks)
        except Exception as e:
            st.error(f"❌ Failed to process {uploaded.name}: {e}")
    return new_chunks


def confidence_html(confidence: str) -> str:
    icons = {"high": "🟢", "medium": "🟡", "low": "🔴", "none": "⚫"}
    return (
        f'<span class="confidence-{confidence}">'
        f'{icons.get(confidence, "?")} {confidence.upper()}</span>'
    )


# ─────────────────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🧠 CiteMind AI</h1>
    <p>Intelligent Research Assistant · Verifiable Citations · Powered by RAG</p>
    <span class="badge">Groq · Gemini · ChromaDB · LangChain</span>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div style="text-align:center; padding:0.5rem 0 1rem 0;">'
        '<h2 style="margin:0;">⚙️ Control Panel</h2>'
        '<small style="color:rgba(255,255,255,0.6);">'
        'CiteMind AI · v1.0</small></div>',
        unsafe_allow_html=True,
    )

    st.markdown('<p class="sidebar-section-title">🤖 Language Model</p>',
                unsafe_allow_html=True)
    provider = st.selectbox(
        "LLM Provider",
        options=["groq", "gemini"],
        format_func=lambda x: {
            "groq": "🚀 Groq · Llama 3.3 70B",
            "gemini": "✨ Gemini · 2.5 Flash",
        }[x],
        label_visibility="collapsed",
    )

    st.markdown('<p class="sidebar-section-title">🔍 Retrieval Tuning</p>',
                unsafe_allow_html=True)
    top_k = st.slider("Top-K results", 1, 10, 5)
    use_mmr = st.checkbox("Use MMR (diversity re-ranking)", value=True)

    st.divider()

    st.markdown('<p class="sidebar-section-title">📤 Upload Documents</p>',
                unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Upload",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploaded_files and st.button("📥 Index Files", use_container_width=True,
                                     type="primary"):
        with st.spinner("Processing documents..."):
            new_chunks = ingest_uploaded_files(uploaded_files)
        if new_chunks > 0:
            st.success(f"✅ Indexed {new_chunks} new chunks!")
            st.rerun()
        else:
            st.info("All files already indexed.")

    st.divider()

    st.markdown('<p class="sidebar-section-title">📊 Index Statistics</p>',
                unsafe_allow_html=True)
    total_chunks = st.session_state.vectorstore.count()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<div class="stat-box"><h2>{total_chunks}</h2>'
            f'<small>Chunks</small></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div class="stat-box"><h2>{len(st.session_state.indexed_files)}</h2>'
            f'<small>Documents</small></div>',
            unsafe_allow_html=True,
        )

    if st.session_state.indexed_files:
        with st.expander("📁 Indexed Files"):
            for f in sorted(st.session_state.indexed_files):
                st.markdown(f"📄 `{f}`")

    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🗑️ Clear Index", use_container_width=True):
            st.session_state.vectorstore.reset()
            st.session_state.indexed_files = set()
            st.session_state.messages = []
            st.rerun()
    with col_b:
        if st.button("🧹 Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()


# ─────────────────────────────────────────────────────────
# Main Chat Area
# ─────────────────────────────────────────────────────────
if total_chunks == 0:
    st.markdown(
        '<div style="text-align:center; padding:1rem; color:rgba(255,255,255,0.85);">'
        '<h3>👋 Welcome to CiteMind AI</h3>'
        '<p>Upload research documents from the sidebar, then ask anything.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(3)
    cards = [
        ("1️⃣", "Upload", "Drag & drop PDF, DOCX, or TXT into the sidebar"),
        ("2️⃣", "Index", "Click <b>Index Files</b> — chunks get embedded"),
        ("3️⃣", "Ask", "Type any research question — get cited answers"),
    ]
    for col, (emoji, title, desc) in zip(cols, cards):
        col.markdown(
            f'<div class="welcome-card">'
            f'<div style="font-size:2rem;">{emoji}</div>'
            f'<h4>{title}</h4><p>{desc}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg["role"] == "user":
                st.markdown(msg["content"])
            else:
                st.markdown(
                    f"**{msg['provider'].upper()}** · "
                    f"Confidence: {confidence_html(msg['confidence'])} · "
                    f"⏱️ {msg['total_time']}s",
                    unsafe_allow_html=True,
                )
                st.markdown(msg["content"])
                if msg.get("citations"):
                    with st.expander(f"📚 Sources ({len(msg['citations'])})"):
                        for c in msg["citations"]:
                            st.markdown(
                                f'<div class="source-card">'
                                f'<b>[{c["id"]}] {c["source"]}</b> · '
                                f'page {c["page"]} '
                                f'<span class="citation-badge">'
                                f'relevance {c["score"]}</span>'
                                f'<br><small>{c["text"][:300]}...</small>'
                                f'</div>',
                                unsafe_allow_html=True,
                            )

    if question := st.chat_input("Ask a question about your documents..."):
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner(f"🤔 Thinking with {provider.upper()}..."):
                engine = get_engine(provider)
                result = engine.ask(question, top_k=top_k, use_mmr=use_mmr)

            st.markdown(
                f"**{result['provider'].upper()}** · "
                f"Confidence: {confidence_html(result['confidence'])} · "
                f"⏱️ {result['total_time']}s",
                unsafe_allow_html=True,
            )
            st.markdown(result["answer"])

            if result["citations"]:
                with st.expander(f"📚 Sources ({len(result['citations'])})"):
                    for c in result["citations"]:
                        st.markdown(
                            f'<div class="source-card">'
                            f'<b>[{c["id"]}] {c["source"]}</b> · '
                            f'page {c["page"]} '
                            f'<span class="citation-badge">'
                            f'relevance {c["score"]}</span>'
                            f'<br><small>{c["text"][:300]}...</small>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )

        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"],
            "provider": result["provider"],
            "confidence": result["confidence"],
            "total_time": result["total_time"],
            "citations": result["citations"],
        })


# ─────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────
st.markdown(
    '<div class="custom-footer">'
    '🧠 <b>CiteMind AI</b> · Crafted with ❤️ by <b>Niam</b><br>'
    '<small>Powered by LangChain · ChromaDB · Groq · Gemini · Sentence-Transformers</small>'
    '</div>',
    unsafe_allow_html=True,
)