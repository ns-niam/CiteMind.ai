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
        E2[384-dim Vector]
    end

    subgraph Storage["💾 Vector Storage"]
        V1[(ChromaDB<br/>Persistent Index)]
    end

    subgraph Retrieval["🔍 Retrieval Engine"]
        R1[Query Embedding]
        R2[Cosine Similarity Search]
        R3[Top-K Retrieval k=5]
        R4[MMR Re-ranking<br/>Diversity boost]
    end

    subgraph Generation["🤖 LLM Generation"]
        G1[Prompt Constructor<br/>Context + Query + Citation rules]
        G2{LLM Router}
        G3[Groq<br/>Llama 3.3 70B]
        G4[Gemini 2.5 Flash]
        G5[Answer + Inline Citations]
    end

    subgraph Eval["📊 Evaluation"]
        EV1[RAGAS Metrics:<br/>Faithfulness<br/>Answer Relevancy<br/>Context Precision]
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
    G5 --> U2

    G5 -.test mode.-> EV1
2. Data Flow Diagram
sequenceDiagram
    actor User
    participant UI as Streamlit UI
    participant Loader as Document Loader
    participant Embed as Embedding Model
    participant DB as ChromaDB
    participant Retr as Retriever
    participant LLM as LLM (Groq/Gemini)

    Note over User,LLM: Phase 1 — Document Ingestion
    User->>UI: Upload research_paper.pdf
    UI->>Loader: Parse document
    Loader->>Loader: Extract text + page numbers
    Loader->>Loader: Split into chunks (1000 chars)
    Loader->>Embed: Encode each chunk
    Embed->>DB: Store vector + metadata
    DB-->>UI: ✅ Ready

    Note over User,LLM: Phase 2 — Question Answering
    User->>UI: "What is the attention mechanism?"
    UI->>Embed: Encode query
    Embed->>Retr: Query vector
    Retr->>DB: Top-K similarity search
    DB-->>Retr: 5 most relevant chunks + metadata
    Retr->>LLM: Context + Query + Citation prompt
    LLM-->>UI: Answer with [Source: paper.pdf, p.4]
    UI-->>User: Display answer + clickable citations
3. Component-Level Architecture
graph LR
    subgraph Frontend
        A[app.py<br/>Streamlit]
    end

    subgraph Source["src/"]
        B[data/<br/>loaders.py<br/>chunker.py]
        C[embeddings/<br/>embedder.py]
        D[retrieval/<br/>vectorstore.py<br/>retriever.py]
        E[generation/<br/>llm.py<br/>prompt.py<br/>citations.py]
        F[evaluation/<br/>ragas_eval.py<br/>metrics.py]
        G[utils/<br/>config.py<br/>logger.py]
    end

    subgraph External["External Services"]
        H[Groq API]
        I[Gemini API]
        J[(ChromaDB<br/>Local)]
    end

    A --> B
    A --> C
    A --> D
    A --> E
    B --> C
    C --> D
    D --> J
    E --> H
    E --> I
    F --> E
    A -.config.-> G
4. Production Deployment Plan
Phase 1 — MVP (Current Project)
Hosting: Streamlit Cloud (free tier)
Vector DB: Local ChromaDB (file-based)
LLM: Groq + Gemini free tier APIs
Limit: ~50 documents, single user
Phase 2 — Scale-Up
Hosting: Docker containers on AWS ECS / Google Cloud Run
Vector DB: Hosted ChromaDB or Pinecone
Caching: Redis for query embedding cache
LLM: Same with rate-limit aware fallback
Phase 3 — Enterprise
Authentication: OAuth2 + per-user document namespaces
Async pipeline: Celery + RabbitMQ for batch ingestion
Monitoring: Prometheus + Grafana dashboards
Vector DB: Distributed Qdrant cluster
graph TB
    subgraph Phase1["Phase 1 — MVP"]
        P1[Streamlit Cloud]
        P1DB[(Local ChromaDB)]
        P1API[Groq + Gemini Free]
    end

    subgraph Phase2["Phase 2 — Scale"]
        P2[Docker on AWS ECS]
        P2DB[(Pinecone)]
        P2C[Redis Cache]
        P2API[Paid API Tier]
    end

    subgraph Phase3["Phase 3 — Enterprise"]
        P3[Kubernetes Cluster]
        P3Auth[OAuth2 + Multi-tenant]
        P3Q[Celery Workers]
        P3DB[(Distributed Qdrant)]
        P3M[Prometheus / Grafana]
    end

    Phase1 --> Phase2 --> Phase3