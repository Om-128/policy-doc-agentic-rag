# PolicyDoc Agentic RAG System

An **Agentic PDF Question–Answering system** designed for **internal knowledge bases**, where the system intelligently decides **when to answer from a vector database** and **when to invoke external tools** if the information is not available locally.

The core focus of this project is **PDF-based knowledge ingestion and retrieval**, combined with **agentic decision-making** using LangChain + LangGraph.

This is a **production‑minded learning project** emphasizing **system design, tool routing, CI/CD, and MLOps trade‑offs**, rather than just LLM prompting.
---

## 🖼️ LangGraph Flowchart
![Flowchart](https://github.com/user-attachments/assets/90d8996b-a6fc-4f4c-96f0-f7fdcbe49c4f)

---

## Demo Video
https://github.com/user-attachments/assets/393724e8-d3c0-4df0-8320-4bf930a9e4d7

---

## 🚀 Key Features

- **PDF‑centric Knowledge Base**: Question answering over internal PDF documents (policies, FAQs, manuals)
- **Agentic Tool Routing**: The agent decides:
  - Use **vector search** when knowledge exists internally
  - Use **external tools / search** when knowledge is missing
- **Chroma Vector Store**: Persistent embeddings for document retrieval
- **Groq‑powered LLMs**: Low‑latency reasoning and response generation
- **Dockerized Backend**: Reproducible, platform‑agnostic runtime
- **CI with GitHub Actions**: Docker build validation on every push
- **Cloud Deployment Exploration**: Render & Hugging Face Spaces (Docker)

---

## 🧠 Architecture Overview

```
User Question
   ↓
Agent (LangGraph)
   ↓
Decision Node
   ├── If answer exists → Vector Retrieval (Chroma)
   └── If missing → External Tool / Search
   ↓
LLM Reasoning (Groq)
   ↓
Final Answer + Source Attribution
```
User Query
   ↓
Flask API (Docker)
   ↓
Agent (LangGraph / LangChain)
   ├── Retrieval Tool → ChromaDB
   └── LLM Reasoning → Groq
   ↓
Final Answer + Sources
```

### Why Agentic RAG?

Traditional RAG pipelines always retrieve documents, even when:
- The answer is already known
- The knowledge base is incomplete

This system instead:
- **Decides whether retrieval is needed**
- Falls back to **external tools** when internal PDFs are insufficient
- Enables more reliable internal knowledge assistants

This pattern closely mirrors **real enterprise knowledge systems**.

---

## 🗂️ Project Structure

```
policy-doc-agentic-rag/
├── .github/workflows/
│   └── ci_cd.yaml            # CI: Docker build validation
├── app/
│   ├── agents/               # Agent & tool definitions
│   ├── config/               # Config loaders
│   ├── ingestion/            # PDF ingestion & vectorstore creation
│   │   ├── pdf_loader.py
│   │   ├── chunking.py
│   │   ├── chroma_store.py
│   │   └── ingestion_pipeline.py
│   └── RAG/                  # Retrieval + embedding logic
│       ├── embedding.py
│       ├── main.py
│       └── utils.py
├── static/                   # Frontend assets (CSS/JS)
├── templates/                # HTML templates
├── data/                     # Local-only PDFs & vectorstore (not in CI/CD)
│   ├── Software_FAQ.pdf
│   └── vectorstore/
├── app.py                    # Flask entrypoint
├── Dockerfile
├── requirements.txt
└── README.md
```
policy-doc-agentic-rag/
├── app/
│   └── frontend/
│       └── app.py          # Flask entrypoint
├── data/                   # (Local only) PDFs & vectorstore
├── Dockerfile
├── requirements.txt        # Runtime dependencies
├── .github/workflows/
│   └── ci.yml              # CI: Docker build check
└── README.md
```

> ⚠️ **Note**: Binary artifacts (PDFs, vectorstores) are intentionally excluded from CI/CD to follow production best practices.

---

## 🐳 Docker Setup

### Build locally
```bash
docker build -t policy-doc-agentic-rag .
```

### Run locally
```bash
docker run -p 7860:7860 \
  -e GROQ_API_KEY=your_key \
  -e TAVILY_API_KEY=your_key \
  -e CHROMA_DB_PATH=/app/vectorstore \
  policy-doc-agentic-rag
```

The app binds to `$PORT` to support cloud platforms.

---

## 🔐 Environment Variables

| Variable | Description |
|-------|------------|
| `GROQ_API_KEY` | Groq API key for LLM inference |
| `TAVILY_API_KEY` | Optional web search tool |
| `CHROMA_DB_PATH` | Path to persisted Chroma vectorstore |
| `MODEL_NAME` | LLM model name (e.g. `llama3-70b-8192`) |

Secrets are injected via the deployment platform and **never committed**.

---

## ⚙️ CI Pipeline (GitHub Actions)

The project includes a minimal but **industry-relevant CI pipeline**:

- Triggered on every push / PR to `main`
- Builds the Docker image
- Fails early on dependency or Dockerfile errors

This ensures that only **buildable artifacts** are deployed.

---

## 🚀 Deployment Notes

### Hugging Face Spaces (Docker)
- Used for ML-friendly memory limits
- Docker SDK provides full runtime control
- Secrets managed via Hugging Face Space settings

### CI/CD Strategy
- **CI**: GitHub Actions validates Docker builds on every push
- **CD**: Deployment experiments explored via Hugging Face Spaces
- Binary artifacts (PDFs, vectorstores) are intentionally excluded from automated deployment

---

## 🧪 Lessons Learned

- Agentic routing improves reliability over static RAG pipelines
- Internal knowledge bases are often incomplete — tool fallback is essential
- Vectorstores and PDFs should be treated as **data**, not Git artifacts
- Free cloud tiers are usually insufficient for PDF‑heavy RAG systems
- CI should validate **code and containers**, not data artifacts

---

## 📌 Future Improvements

- Metadata-aware retrieval
- Lazy-loading vectorstores
- Monitoring (latency, token usage)
- Security hardening (prompt injection, tool access control)

---

## 👤 Author

**Om Tambat**  
AI / ML Engineer (in transition)  

This project is part of a hands-on journey into **Agentic AI systems, MLOps, and real-world deployment challenges**.

---

## 🔗 Useful Links

- **LangGraph (Agent Flow Framework)**  
  https://langchain-ai.github.io/langgraph/

- **Demo Video**  
  _Coming soon — will showcase PDF ingestion, agent routing, and tool fallback_

---

## ⭐ If You’re Reviewing This Repo

This project intentionally focuses on:
- Internal PDF-based knowledge systems
- Agentic decision-making (retrieve vs tool use)
- Real-world CI/CD and deployment constraints

Rather than just prompt engineering or model benchmarks.

Thanks for reviewing 🙌
