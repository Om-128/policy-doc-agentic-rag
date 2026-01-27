# PolicyDoc Agentic RAG System

An **Agentic Retrieval-Augmented Generation (RAG)** system for querying policy / FAQ documents using **LangChain**, **Groq LLMs**, and **ChromaDB**, packaged in a **Docker-first** architecture with **CI via GitHub Actions** and deployment experiments on **Hugging Face Spaces**.

This project is designed as a **production-minded learning project** focusing on **system design, CI/CD, and MLOps trade-offs**, not just model inference.

---

## 🚀 Key Features

* **Agentic RAG**: Uses LangChain agents to decide when to retrieve, reason, or respond
* **Chroma Vector Store**: Persistent vector search for policy/FAQ documents
* **Groq-powered LLMs**: Fast inference using Groq-hosted models
* **Dockerized Backend**: Reproducible builds and environment parity
* **CI with GitHub Actions**: Docker build validation on every push
* **Cloud Deployment Exploration**: Render & Hugging Face Spaces (Docker)

---

## 🧠 Architecture Overview

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

Instead of a simple "retrieve → answer" pipeline, the system:

* Decides **when retrieval is needed**
* Can chain multiple reasoning steps
* Is extensible to tools (search, validators, policies)

---

## 🗂️ Project Structure

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

| Variable         | Description                             |
| ---------------- | --------------------------------------- |
| `GROQ_API_KEY`   | Groq API key for LLM inference          |
| `TAVILY_API_KEY` | Optional web search tool                |
| `CHROMA_DB_PATH` | Path to persisted Chroma vectorstore    |
| `MODEL_NAME`     | LLM model name (e.g. `llama3-70b-8192`) |

Secrets are injected via the deployment platform and **never committed**.

---

## ⚙️ CI Pipeline (GitHub Actions)

The project includes a minimal but **industry-relevant CI pipeline**:

* Triggered on every push / PR to `main`
* Builds the Docker image
* Fails early on dependency or Dockerfile errors

This ensures that only **buildable artifacts** are deployed.

---

## 🚀 Deployment Notes

### Hugging Face Spaces (Docker)

* Chosen for ML-friendly memory limits
* Docker SDK used for full control
* Environment variables managed via HF Secrets

### Why Vectorstores Are Not in Git

* Binary artifacts (PDFs, `.bin`, `.sqlite`) are not suitable for Git
* In real systems, these live in object storage or are rebuilt
* This project explicitly demonstrates that separation

---

## 🧪 Lessons Learned

* Runtime type selection is immutable on many PaaS platforms
* Free tiers are often insufficient for RAG systems
* CI should validate builds, not deploy data
* ML systems require separating **code**, **data**, and **infrastructure**

---

## 📌 Future Improvements

* Metadata-aware retrieval
* Lazy-loading vectorstores
* Monitoring (latency, token usage)
* Security hardening (prompt injection, tool access control)

---

## 👤 Author

**Om Tambat**
AI / ML Engineer (in transition)

This project is part of a hands-on journey into **Agentic AI systems, MLOps, and real-world deployment challenges**.

---

## ⭐ If You’re Reviewing This Repo

This project intentionally focuses on:

* Engineering trade-offs
* Deployment realism
* Clean system design

Not just model accuracy.

Thanks for reading 🙌
