"""
Run full evaluation on test queries.
Saves results to data/processed/eval_results.json
Run: python -m tests.run_evaluation
"""
import sys, os, json
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.ingest import ingest_directory
from src.retrieval.vectorstore import VectorStore
from src.generation.rag_engine import RAGEngine
from src.evaluation.evaluator import RAGEvaluator
from tests.eval_queries import EVAL_QUERIES


def main():
    print("=" * 70)
    print("📊 CiteMind AI - RAG Evaluation Suite")
    print("=" * 70)

    # Ensure index ready
    vs = VectorStore()
    if vs.count() == 0:
        print("\n📦 Building index...")
        ingest_directory("data/raw", reset=False)

    print(f"\n✅ {vs.count()} chunks indexed")
    print(f"📋 {len(EVAL_QUERIES)} eval queries\n")

    evaluator = RAGEvaluator()
    all_results = {"groq": [], "gemini": []}

    for provider in ["groq", "gemini"]:
        print("\n" + "=" * 70)
        print(f"🤖 Evaluating with {provider.upper()}")
        print("=" * 70)
        engine = RAGEngine(llm_provider=provider)

        for i, item in enumerate(EVAL_QUERIES, start=1):
            q, gt = item["question"], item["ground_truth"]
            print(f"\n[{i}/{len(EVAL_QUERIES)}] {q[:60]}...")

            res = engine.ask(q)
            contexts = [c["text"] for c in res["citations"]]
            metrics = evaluator.evaluate_one(q, res["answer"], contexts, gt)

            print(
                f"   📊 Relevancy: {metrics['answer_relevancy']} | "
                f"Correctness: {metrics['answer_correctness']} | "
                f"Precision: {metrics['context_precision']} | "
                f"Faithfulness: {metrics['faithfulness']}"
            )

            all_results[provider].append({
                "question": q,
                "ground_truth": gt,
                "answer": res["answer"],
                "confidence": res["confidence"],
                "total_time": res["total_time"],
                "citations": [
                    {"source": c["source"], "page": c["page"], "score": c["score"]}
                    for c in res["citations"]
                ],
                **metrics,
            })

    # Summary
    print("\n\n" + "=" * 70)
    print("📈 AGGREGATE RESULTS")
    print("=" * 70)
    summary = {}
    for provider in ["groq", "gemini"]:
        agg = evaluator.evaluate_batch(all_results[provider])
        summary[provider] = agg
        avg_time = round(
            sum(r["total_time"] for r in all_results[provider]) / len(all_results[provider]), 2
        )
        agg["avg_response_time"] = avg_time
        print(f"\n{provider.upper()}:")
        for k, v in agg.items():
            print(f"  {k:25s}: {v}")

    # Save results
    out_dir = Path("data/processed")
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "eval_results.json", "w") as f:
        json.dump({"per_query": all_results, "summary": summary}, f, indent=2)

    print(f"\n💾 Results saved to data/processed/eval_results.json")
    print("\n🎉 Evaluation complete!")


if __name__ == "__main__":
    main()