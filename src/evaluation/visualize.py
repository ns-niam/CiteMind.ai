"""
CiteMind AI - Evaluation Visualizations
Generates charts for the report and presentation.
"""
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

plt.style.use("seaborn-v0_8-darkgrid")

OUT_DIR = Path("assets/charts")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_results():
    with open("data/processed/eval_results.json") as f:
        return json.load(f)


def chart_metrics_comparison(data):
    """Bar chart: Groq vs Gemini on all metrics."""
    metrics = ["answer_relevancy", "answer_correctness",
               "context_precision", "faithfulness"]
    labels = ["Answer\nRelevancy", "Answer\nCorrectness",
              "Context\nPrecision", "Faithfulness"]

    groq_vals = [data["summary"]["groq"][m] for m in metrics]
    gemini_vals = [data["summary"]["gemini"][m] for m in metrics]

    x = np.arange(len(metrics))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    b1 = ax.bar(x - width/2, groq_vals, width, label="Groq (Llama 3.3 70B)",
                color="#667eea", edgecolor="white")
    b2 = ax.bar(x + width/2, gemini_vals, width, label="Gemini 2.5 Flash",
                color="#764ba2", edgecolor="white")

    ax.set_ylabel("Score (0-1)", fontsize=12)
    ax.set_title("CiteMind AI — RAG Evaluation Metrics",
                 fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 1.05)
    ax.legend(loc="lower right")

    for bars in [b1, b2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 0.01,
                    f"{height:.2f}", ha="center", fontweight="bold")

    plt.tight_layout()
    plt.savefig(OUT_DIR / "01_metrics_comparison.png", dpi=150)
    plt.close()
    print(f"  ✅ {OUT_DIR}/01_metrics_comparison.png")


def chart_response_times(data):
    """Latency comparison."""
    providers = ["Groq", "Gemini"]
    times = [data["summary"]["groq"]["avg_response_time"],
             data["summary"]["gemini"]["avg_response_time"]]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(providers, times, color=["#667eea", "#764ba2"],
                  edgecolor="white", width=0.5)
    ax.set_ylabel("Avg Response Time (seconds)", fontsize=12)
    ax.set_title("Average End-to-End Response Time",
                 fontsize=14, fontweight="bold")
    for bar, t in zip(bars, times):
        ax.text(bar.get_x() + bar.get_width()/2, t + 0.05,
                f"{t}s", ha="center", fontweight="bold")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "02_response_times.png", dpi=150)
    plt.close()
    print(f"  ✅ {OUT_DIR}/02_response_times.png")


def chart_per_query_faithfulness(data):
    """Per-query faithfulness scores."""
    groq_q = data["per_query"]["groq"]
    gemini_q = data["per_query"]["gemini"]

    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(groq_q))
    width = 0.35

    ax.bar(x - width/2, [r["faithfulness"] for r in groq_q],
           width, label="Groq", color="#667eea")
    ax.bar(x + width/2, [r["faithfulness"] for r in gemini_q],
           width, label="Gemini", color="#764ba2")

    ax.set_xlabel("Query #", fontsize=11)
    ax.set_ylabel("Faithfulness Score", fontsize=11)
    ax.set_title("Per-Query Faithfulness Scores",
                 fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels([f"Q{i+1}" for i in range(len(groq_q))])
    ax.set_ylim(0, 1.0)
    ax.legend()
    ax.axhline(y=0.85, color="green", linestyle="--", alpha=0.5,
               label="Target (0.85)")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "03_per_query_faithfulness.png", dpi=150)
    plt.close()
    print(f"  ✅ {OUT_DIR}/03_per_query_faithfulness.png")


def chart_confidence_distribution(data):
    """Pie chart of confidence levels."""
    all_confidences = []
    for prov in ["groq", "gemini"]:
        all_confidences.extend([r["confidence"] for r in data["per_query"][prov]])
    counts = {c: all_confidences.count(c) for c in ["high", "medium", "low", "none"]}

    fig, ax = plt.subplots(figsize=(7, 7))
    colors = ["#4ade80", "#fbbf24", "#f87171", "#94a3b8"]
    labels = [f"{k.capitalize()} ({v})" for k, v in counts.items() if v > 0]
    sizes = [v for v in counts.values() if v > 0]
    used_colors = [colors[i] for i, v in enumerate(counts.values()) if v > 0]

    ax.pie(sizes, labels=labels, colors=used_colors, autopct="%1.0f%%",
           startangle=90, textprops={"fontweight": "bold"})
    ax.set_title("Confidence Level Distribution",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "04_confidence_distribution.png", dpi=150)
    plt.close()
    print(f"  ✅ {OUT_DIR}/04_confidence_distribution.png")


def chart_radar(data):
    """Radar chart: multi-metric profile."""
    metrics = ["answer_relevancy", "answer_correctness",
               "context_precision", "faithfulness"]
    labels = ["Relevancy", "Correctness", "Precision", "Faithfulness"]

    angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
    angles += angles[:1]

    groq_vals = [data["summary"]["groq"][m] for m in metrics]
    gemini_vals = [data["summary"]["gemini"][m] for m in metrics]
    groq_vals += groq_vals[:1]
    gemini_vals += gemini_vals[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.plot(angles, groq_vals, "o-", linewidth=2, label="Groq", color="#667eea")
    ax.fill(angles, groq_vals, alpha=0.25, color="#667eea")
    ax.plot(angles, gemini_vals, "o-", linewidth=2, label="Gemini", color="#764ba2")
    ax.fill(angles, gemini_vals, alpha=0.25, color="#764ba2")

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=11)
    ax.set_ylim(0, 1)
    ax.set_title("RAG Quality Profile", fontsize=14, fontweight="bold", pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.2, 1.1))
    plt.tight_layout()
    plt.savefig(OUT_DIR / "05_radar_chart.png", dpi=150)
    plt.close()
    print(f"  ✅ {OUT_DIR}/05_radar_chart.png")


def main():
    print("📊 Generating evaluation charts...")
    data = load_results()
    chart_metrics_comparison(data)
    chart_response_times(data)
    chart_per_query_faithfulness(data)
    chart_confidence_distribution(data)
    chart_radar(data)
    print(f"\n🎉 All charts saved to {OUT_DIR}/")


if __name__ == "__main__":
    main()