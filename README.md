# Cortex RAG – AI-Driven Security Copilot for Threat Investigation

Cortex RAG is a **Retrieval‑Augmented Generation (RAG)** platform for **cybersecurity**. 
It ingests **MITRE ATT&CK**, **Sigma/YARA**, and **SIEM alert** data, indexes it into a **vector store**, 
and exposes a **Copilot-style chat** so analysts can ask natural‑language questions, triage incidents, 
map techniques, and generate executive/technical reports with citations.

## Features
- 🔎 **Semantic search over security knowledge** (embeddings + vector DB)
- 🤖 **Agentic LLMs** for triage, correlation, and reporting
- 🧠 **Multi‑model** (GPT‑4 / Claude / Llama‑3 / Mistral) with routing
- 📊 **RAG evaluation** (faithfulness, relevance, latency, cost)
- ⚙️ **FastAPI backend**, **Streamlit UI**, Dockerized and AWS‑ready

## Repo Layout
```
api/        # FastAPI service (endpoints, orchestration, tools)
ingest/     # ETL for ATT&CK, Sigma/YARA, SIEM samples
indexer/    # Embeddings + vector indexing (FAISS/OpenSearch)
ui/         # Streamlit chat app + metrics dashboards
eval/       # RAG evaluation (Ragas/TruLens), reports
notebooks/  # Exploration notebooks
data/       # raw/ and processed/ (large files kept out of git)
docker/     # Dockerfiles and compose
scripts/    # CLI helpers (seed, run, demo)
docs/       # Diagrams, design notes
.github/workflows/ # CI: lint + tests
```

## Quickstart (Local)
```bash
python -m venv .venv && source .venv/bin/activate   # (Windows: .\.venv\Scripts\Activate.ps1)
pip install -r requirements.txt

# Run API and UI in two terminals
uvicorn api.main:app --reload --port 8000
streamlit run ui/app.py
```

## Deployment (Sketch)
- Vectors: OpenSearch Serverless (AWS) or FAISS locally
- Storage: S3
- Compute: ECS Fargate (API), Streamlit via ECS/EC2/CloudFront
- Observability: CloudWatch

## Security
- Keep secrets in environment variables or GitHub Actions **Secrets**
- Prompt‑injection and PII‑redaction guards (to be wired in API)
- See [SECURITY.md](SECURITY.md)

## License
MIT
