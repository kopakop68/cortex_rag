from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Cortex RAG API")

class Query(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(q: Query):
    # TODO: wire retriever + LLM; return citations
    return {"answer": f"(placeholder) You asked: {q.question}", "citations": []}
