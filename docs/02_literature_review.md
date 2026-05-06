# CiteMind AI — Literature Review

## Overview

This document surveys five foundational works that directly inform the CiteMind AI design.

---

## 1. Lewis et al. (2020) — "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"

**Venue:** NeurIPS 2020
**Link:** https://arxiv.org/abs/2005.11401

**Key Contribution:** Introduced the RAG framework — combining a parametric memory (pre-trained seq2seq model) with a non-parametric memory (dense vector index of Wikipedia). Achieved state-of-the-art on open-domain QA.

**Relevance to CiteMind:** Foundational paper defining the RAG paradigm we build on.

**How we differ:** We focus on user-uploaded research documents (not a static Wikipedia index) and add explicit citation tracking.

---

## 2. Karpukhin et al. (2020) — "Dense Passage Retrieval for Open-Domain QA"

**Venue:** EMNLP 2020
**Link:** https://arxiv.org/abs/2004.04906

**Key Contribution:** Showed that dense embeddings (dual-encoders) significantly outperform BM25/TF-IDF retrieval for QA tasks.

**Relevance to CiteMind:** Justifies our use of `sentence-transformers` over keyword-based retrieval.

**How we differ:** We use pre-trained MiniLM (lightweight) instead of training a custom dual-encoder.

---

## 3. Reimers & Gurevych (2019) — "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks"

**Venue:** EMNLP 2019
**Link:** https://arxiv.org/abs/1908.10084

**Key Contribution:** Introduced Sentence-BERT for efficient semantic similarity at sentence level.

**Relevance to CiteMind:** The `all-MiniLM-L6-v2` model we use is a direct descendant.

**How we differ:** We apply it to document-chunk retrieval, not sentence-pair similarity.

---

## 4. Es et al. (2023) — "RAGAS: Automated Evaluation of Retrieval Augmented Generation"

**Venue:** EACL 2024
**Link:** https://arxiv.org/abs/2309.15217

**Key Contribution:** Reference-free metrics (Faithfulness, Answer Relevancy, Context Precision) for RAG.

**Relevance to CiteMind:** Our primary evaluation framework.

**How we differ:** Applied to research-document QA, not general benchmarks.

---

## 5. Gao et al. (2023) — "Retrieval-Augmented Generation for Large Language Models: A Survey"

**Venue:** arXiv 2023
**Link:** https://arxiv.org/abs/2312.10997

**Key Contribution:** Categorizes RAG into Naive, Advanced, and Modular paradigms; identifies key challenges.

**Relevance to CiteMind:** Provides the design vocabulary; CiteMind implements **Advanced RAG** with chunking and citation re-ranking.

**How we differ:** Focus on the citation-tracking sub-problem, identified as under-explored.

---

## Comparison Table

| System | Open-Source | Citations | Multi-LLM | User Documents | Evaluation |
|--------|-------------|-----------|-----------|----------------|------------|
| ChatGPT (vanilla) | ❌ | ❌ | ❌ | ❌ | — |
| Perplexity AI | ❌ | ✅ | ❌ | ❌ | — |
| NotebookLM (Google) | ❌ | ✅ | ❌ | ✅ | — |
| **CiteMind AI (ours)** | ✅ | ✅ | ✅ | ✅ | ✅ RAGAS |

## Gap We Address

While Perplexity and NotebookLM offer some features, **no fully open-source, self-hostable system** combines:
- Multi-LLM fallback architecture
- Explicit RAGAS-based evaluation
- User-uploaded research document focus

CiteMind AI fills this gap.