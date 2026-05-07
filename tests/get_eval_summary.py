"""Quick utility to print eval summary for the report."""
import json

with open("data/processed/eval_results.json") as f:
    data = json.load(f)

s = data["summary"]
print("\n" + "=" * 60)
print("📊 EVAL SUMMARY (copy these into FINAL_REPORT.md)")
print("=" * 60)
for provider in ["groq", "gemini"]:
    print(f"\n{provider.upper()}:")
    for k, v in s[provider].items():
        print(f"  {k:25s}: {v}")