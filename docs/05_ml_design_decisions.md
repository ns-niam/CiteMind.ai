# CiteMind AI — ML Design Decisions

## 1. Algorithm Choices & Justification

### 1.1 Embedding Model: `sentence-transformers/all-MiniLM-L6-v2`

| Criterion | Why This Choice |
|-----------|----------------|
| **Speed** | 384-dim vectors → 10x faster than BERT-base (768-dim) |
| **Size** | Only 80MB → runs on CPU without GPU |
| **Quality** | Top-tier on MTEB benchmark for retrieval tasks |
| **License** | Apache 2.0 — free for commercial use |

**Alternatives considered:**
- ❌ `text-embedding-ada-002` (OpenAI) — paid, vendor lock-in
- ❌ `BAAI/bge-large-en` — slower, marginal accuracy gain
- ✅ `all-MiniLM-L6-v2` — best speed/quality tradeoff for CPU-only setup

### 1.2 Vector Database: ChromaDB

| Criterion | Why This Choice |
|-----------|----------------|
| **Local-first** | No external service required |
| **Persistence** | Built-in disk storage |
| **Python-native** | Direct integration with LangChain |
| **Free** | No license cost |

**Alternatives considered:**
- ❌ Pinecone — paid after free tier
- ❌ Weaviate — more complex setup
- ❌ FAISS — no built-in metadata filtering
- ✅ ChromaDB — perfect for MVP

### 1.3 Chunking Strategy: Recursive Character Splitter

- **Chunk size:** 1000 characters
- **Overlap:** 200 characters (20%)
- **Why recursive:** Respects paragraph and sentence boundaries
- **Why these numbers:** Empirically optimal for academic papers (long-form content)

### 1.4 Retrieval: Top-K + MMR

- **Top-K = 5:** Balance between context window and noise
- **MMR (λ=0.5):** Reduces redundancy when multiple chunks repeat info
- **Justification:** RAGAS-tunable hyperparameters

### 1.5 LLM: Dual Provider (Groq + Gemini)

| Provider | Strength | Use Case |
|----------|----------|----------|
| **Groq (Llama 3.3 70B)** | Ultra-low latency (~500ms) | Quick queries |
| **Gemini 2.5 Flash** | Better reasoning, longer context | Complex queries |

**Routing strategy:** User can pick; default = Groq for speed.

## 2. Evaluation Metrics

### 2.1 RAGAS Metrics

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| **Faithfulness** | Does the answer match retrieved context? | > 0.85 |
| **Answer Relevancy** | Does the answer address the question? | > 0.80 |
| **Context Precision** | Are retrieved chunks actually relevant? | > 0.75 |
| **Context Recall** | Did we retrieve all needed info? | > 0.70 |

### 2.2 System Metrics

| Metric | Target | Why |
|--------|--------|-----|
| **End-to-end latency** | < 5s | User experience |
| **Retrieval latency** | < 200ms | Most of time should be LLM |
| **Index build time** | < 1s/page | Acceptable for ingestion |

## 3. Data Strategy

### Data Sources
- **Primary:** User-uploaded documents (PDF, DOCX, TXT)
- **Test set:** Open-access papers from arXiv (CS, ML categories)
- **Eval queries:** 30 hand-crafted queries with ground truth

### Preprocessing
1. Text extraction with layout preservation (`pdfplumber`)
2. Removal of headers/footers/page numbers (regex)
3. Unicode normalization
4. Chunk-level metadata: `{doc_id, page, chunk_idx, source_filename}`

## 4. Trade-offs Acknowledged

| Trade-off | Choice | Reason |
|-----------|--------|--------|
| Speed vs Accuracy | Speed-first | User-facing tool needs <5s response |
| Local vs Cloud | Local DB | Privacy-friendly for academic use |
| Open-source vs Paid | Open-source | Educational accessibility |
| Single LLM vs Multi-LLM | Multi-LLM | Reliability + comparison |