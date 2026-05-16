# CiteMind AI — System Architecture

## 1. End-to-End System Architecture

```mermaid
flowchart TB

    subgraph User["👤 User Layer"]
        U1[Researcher / Student]
        U2[Streamlit Web UI]
    end

    subgraph Ingestion["📥 Document Ingestion Pipeline"]
        D1[PDF / DOCX / TXT Upload]
        D2[Document Loader<br/>pdfplumber / python-docx]
        D3[Text Cleaner<br/>Remove headers, footers, noise]
        D4[Recursive Text Splitter<br/>chunk_size=1000, overlap=200]
        D5[Metadata Tagger<br/>doc_id, page, chunk_id]
    end

    subgraph Embedding["🧮 Embedding Layer"]
        E1[Sentence-Transformers<br/>all-MiniLM-L6-v2]
        E2[384-dim Vector Embeddings]
    end

    subgraph Storage["💾 Vector Storage"]
        V1[(ChromaDB<br/>Persistent Vector Index)]
    end

    subgraph Retrieval["🔍 Retrieval Engine"]
        R1[Query Embedding]
        R2[Cosine Similarity Search]
        R3[Top-K Retrieval k=5]
        R4[MMR Re-ranking<br/>Diversity Optimization]
    end

    subgraph Generation["🤖 LLM Generation Layer"]
        G1[Prompt Constructor<br/>Context + Query + Citation Rules]
        G2{LLM Router}
        G3[Groq<br/>Llama 3.3 70B]
        G4[Gemini 2.5 Flash]
        G5[Answer + Inline Citations]
    end

    subgraph ML["🧠 ML Confidence Layer"]
        M1[Feature Extraction]
        M2[RandomForest Classifier]
        M3[Confidence Prediction<br/>HIGH / MEDIUM / LOW]
    end

    subgraph Eval["📊 Evaluation Pipeline"]
        EV1[RAGAS Metrics<br/>Faithfulness<br/>Answer Relevancy<br/>Context Precision]
        EV2[MLflow Experiment Tracking]
    end

    U1 --> U2
    U2 --> D1

    D1 --> D2 --> D3 --> D4 --> D5
    D5 --> E1 --> E2
    E2 --> V1

    U2 -- User Query --> R1
    R1 --> R2
    V1 --> R2

    R2 --> R3 --> R4
    R4 --> G1 --> G2

    G2 --> G3
    G2 --> G4

    G3 --> G5
    G4 --> G5

    G5 --> M1 --> M2 --> M3
    M3 --> U2

    G5 -. Evaluation .-> EV1
    EV1 --> EV2
```

---

## 2. Data Flow Diagram

```mermaid
sequenceDiagram

    actor User
    participant UI as Streamlit UI
    participant Loader as Document Loader
    participant Embed as Embedding Model
    participant DB as ChromaDB
    participant Retr as Retriever
    participant LLM as Groq / Gemini
    participant ML as Confidence Model

    Note over User,ML: Phase 1 — Document Ingestion

    User->>UI: Upload research_paper.pdf
    UI->>Loader: Parse document
    Loader->>Loader: Extract text + metadata
    Loader->>Loader: Split into semantic chunks
    Loader->>Embed: Generate embeddings
    Embed->>DB: Store vectors + metadata
    DB-->>UI: Documents indexed successfully

    Note over User,ML: Phase 2 — Retrieval + Generation

    User->>UI: Ask research question
    UI->>Embed: Encode query embedding
    Embed->>Retr: Query vector
    Retr->>DB: Semantic similarity search
    DB-->>Retr: Top-K relevant chunks
    Retr->>LLM: Context + Query + Citation Prompt

    LLM-->>ML: Generated answer
    ML-->>UI: Confidence prediction
    UI-->>User: Final answer + citations + confidence
```

---

## 3. Component-Level Architecture

```mermaid
graph LR

    subgraph Frontend
        A[app.py<br/>Streamlit Web App]
    end

    subgraph Source["src/"]
        B[data/<br/>loader.py<br/>chunker.py<br/>ingest.py]

        C[embeddings/<br/>embedder.py]

        D[retrieval/<br/>vectorstore.py<br/>retriever.py]

        E[generation/<br/>llm.py<br/>prompts.py<br/>citations.py<br/>rag_engine.py]

        F[ml/<br/>feature_builder.py<br/>train_confidence.py<br/>confidence_runtime.py]

        G[evaluation/<br/>evaluator.py<br/>visualize.py]

        H[utils/<br/>config.py<br/>display.py]
    end

    subgraph External["External Services"]
        I[Groq API]
        J[Gemini API]
        K[(ChromaDB)]
        L[(MLflow)]
    end

    A --> B
    A --> C
    A --> D
    A --> E
    A --> F

    B --> C
    C --> D
    D --> K

    E --> I
    E --> J

    F --> E
    G --> E

    G --> L

    A -. Config .-> H
```

---

## 4. Production Deployment Roadmap

### 🚀 Phase 1 — MVP (Current System)

| Component | Technology |
| --- | --- |
| Frontend | Streamlit Cloud |
| Vector DB | Local ChromaDB |
| LLM APIs | Groq + Gemini |
| Storage | Local persistent index |
| Scale | Single-user / small dataset |

---

### ⚡ Phase 2 — Scale-Up Architecture

| Component | Technology |
| --- | --- |
| Deployment | Docker + AWS ECS / Cloud Run |
| Vector DB | Pinecone / Hosted ChromaDB |
| Caching | Redis |
| API Layer | FastAPI |
| Scaling | Multi-user support |

---

### 🏢 Phase 3 — Enterprise Architecture

| Component | Technology |
| --- | --- |
| Orchestration | Kubernetes |
| Authentication | OAuth2 + RBAC |
| Task Queue | Celery + RabbitMQ |
| Monitoring | Prometheus + Grafana |
| Vector DB | Distributed Qdrant Cluster |
| Multi-Tenancy | Per-user namespaces |

---

## 5. Architectural Highlights

- Hybrid ML + RAG architecture
- Semantic retrieval with vector embeddings
- Citation-aware grounded generation
- Dual LLM routing (Groq + Gemini)
- ML-based confidence prediction
- Experiment tracking using MLflow
- Docker-ready deployment strategy
- Scalable future enterprise roadmap
