"""
CiteMind AI - Citation Tracker
Formats retrieved chunks into citation-ready context.
"""
from typing import List, Dict, Tuple


class CitationTracker:
    """Tracks and formats sources for inclusion in LLM answers."""

    @staticmethod
    def format_context(chunks: List[Dict]) -> Tuple[str, List[Dict]]:
        """
        Build a context string with [Source N] tags + a citation list.
        Returns: (context_string, citations_list)
        """
        context_parts = []
        citations = []

        for i, chunk in enumerate(chunks, start=1):
            meta = chunk["metadata"]
            tag = f"[Source {i}]"
            context_parts.append(
                f"{tag} (from {meta['source']}, page {meta['page']}):\n"
                f"{chunk['text']}\n"
            )
            citations.append({
                "id": i,
                "source": meta["source"],
                "page": meta["page"],
                "score": round(chunk.get("score", 0), 3),
                "text": chunk["text"],
            })

        return "\n---\n".join(context_parts), citations

    @staticmethod
    def format_citations_for_display(citations: List[Dict]) -> str:
        """Pretty-print citations for terminal/text display."""
        lines = ["\n📚 Sources:"]
        for c in citations:
            lines.append(
                f"  [{c['id']}] {c['source']}, page {c['page']} "
                f"(relevance: {c['score']})"
            )
        return "\n".join(lines)