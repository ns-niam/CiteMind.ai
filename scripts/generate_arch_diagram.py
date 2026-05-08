"""Generate architecture diagram for the presentation."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from pathlib import Path

fig, ax = plt.subplots(figsize=(14, 7))
ax.set_xlim(0, 14)
ax.set_ylim(0, 7)
ax.axis("off")
fig.patch.set_facecolor("#0f0c29")
ax.set_facecolor("#0f0c29")

def box(x, y, w, h, label, color="#667eea"):
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                          linewidth=2, edgecolor="white",
                          facecolor=color, alpha=0.85)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, label, ha="center", va="center",
            color="white", fontsize=11, fontweight="bold")

def arrow(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color="#a8edea", lw=2))

# Top row — ingestion
box(0.3, 5.5, 1.8, 1, "📄 PDF/DOCX/TXT", "#764ba2")
box(2.5, 5.5, 1.8, 1, "Loader\n+ Cleaner", "#667eea")
box(4.7, 5.5, 1.8, 1, "Chunker\n(1000/200)", "#667eea")
box(6.9, 5.5, 1.8, 1, "Embedder\nMiniLM-L6", "#667eea")
box(9.1, 5.5, 1.8, 1, "ChromaDB\n(HNSW)", "#a8edea")

arrow(2.1, 6.0, 2.5, 6.0)
arrow(4.3, 6.0, 4.7, 6.0)
arrow(6.5, 6.0, 6.9, 6.0)
arrow(8.7, 6.0, 9.1, 6.0)

# Middle - Query
box(0.3, 3.0, 1.8, 1, "❓ User Query", "#764ba2")
box(2.5, 3.0, 1.8, 1, "Query\nEmbedder", "#667eea")
box(4.7, 3.0, 1.8, 1, "Retriever\n(Top-K + MMR)", "#667eea")
box(6.9, 3.0, 1.8, 1, "Citation\nFormatter", "#667eea")

arrow(2.1, 3.5, 2.5, 3.5)
arrow(4.3, 3.5, 4.7, 3.5)
arrow(6.5, 3.5, 6.9, 3.5)
arrow(10.0, 5.5, 5.6, 4.0)  # DB to retriever

# LLM
box(9.1, 3.0, 1.8, 1, "Groq\nLlama 3.3", "#a8edea")
box(11.3, 3.0, 1.8, 1, "Gemini\n2.5 Flash", "#a8edea")
arrow(8.7, 3.5, 9.1, 3.5)
arrow(8.7, 3.3, 11.3, 3.3)

# Output
box(5.5, 0.7, 5.0, 1, "💬 Answer + [Source N] Citations\n+ Confidence (🟢/🟡/🔴)",
    "#fed6e3")
arrow(10.0, 3.0, 8.0, 1.7)
arrow(11.7, 3.0, 8.0, 1.7)

# Title
ax.text(7, 6.9, "CiteMind AI — End-to-End RAG Pipeline",
        ha="center", color="#a8edea", fontsize=18, fontweight="bold")

plt.tight_layout()
out = Path("assets/charts/architecture_diagram.png")
out.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(out, dpi=150, facecolor="#0f0c29")
print(f" Saved {out}")