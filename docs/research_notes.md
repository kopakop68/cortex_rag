# Cortex RAG — Research Notes (Day 2)
_Last updated: 2025-11-01_

## 1. What is RAG (Retrieval‑Augmented Generation)?
RAG = **Retriever + Generator**. A retriever fetches small, relevant chunks from a knowledge base; a generator (LLM) uses those chunks as context to produce grounded answers **with citations**.

**Flow:**
1) Ingest → clean/normalize → chunk  
2) Create **embeddings** (vectors) for each chunk  
3) Store vectors in a **vector index** (FAISS → OpenSearch)  
4) At query time: embed question → **semantic search** → top‑k chunks  
5) Prompt LLM with those chunks → answer + **citations**

## 2. Embeddings (model choices)
Start: `sentence-transformers/all-mpnet-base-v2`  
Benchmark later: `intfloat/e5-base-v2`, `bge-base-en-v1.5`.

**Chunking tips:** 700–1000 tokens, preserve headings, keep metadata: `source`, `doc_type`, `tactic`, `technique_id`, etc.

## 3. Vector Store
- **Phase 1:** FAISS (local, simple, fast)  
- **Phase 2:** AWS OpenSearch (managed vectors, IAM, scaling)

## 4. LLMs & Routing
Begin with a high‑quality closed model for final answers; consider smaller open models for extraction tasks. Add a router later.

## 5. Evaluation (RAGAS / TruLens)
- Faithfulness, Context Precision/Recall, Answer Relevance, Latency/Cost  
- Build a **gold set** (~30 questions) and a small **judging rubric**.

## 6. Security Use‑Cases
- Triage alerts → map to ATT&CK techniques  
- Hunt hypotheses → suggest Sigma rules  
- Executive & analyst reports with citations  
- Recommend mitigations/detections

## 7. Risks & Mitigations
Hallucination (citations & prompts), Prompt injection (guards), PII leakage (redaction), Cost creep (routing & caching).

### Prompt (draft)
```
You are a Security Copilot. Answer using ONLY the supplied context.
Cite sources as [#] with doc_type and technique_id if present.
Question: {question}

Context:
{context}

Answer concisely. End with citations like [attack:T1059], [sigma:proc_rule].
```
