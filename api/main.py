from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Any, Dict, List
import os
from dotenv import load_dotenv

from indexer.retriever import Retriever
from api.llm import chat_once
from api.prompt_templates import SYSTEM_PROMPT, build_user_prompt

load_dotenv()
app = FastAPI()

retriever = None

class AskRequest(BaseModel):
    q: str = Field(alias="question")
    k: int = 5
    min_score: float = 0.0
    doc_type: str = "any"
    model_config = {"populate_by_name": True, "extra": "ignore"}

@app.on_event("startup")
async def _startup():
    global retriever
    try:
        retriever = Retriever()
        print("[API] Retriever loaded for /ask")
        print("[API] main.py path:", __file__)
    except Exception as e:
        print("[API] Retriever NOT loaded:", e)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/ask")
async def ask(req: AskRequest):
    if retriever is None:
        return {"answer": "Index not loaded. Build index and restart API.", "results": []}
    hits = retriever.search(req.q, req.k, req.min_score, req.doc_type)
    if not hits:
        return {"answer": "Insufficient context to answer reliably.", "results": []}
    user_prompt = build_user_prompt(req.q, hits)
    answer = chat_once(SYSTEM_PROMPT, user_prompt, os.getenv("GROQ_MODEL"))
    return {"answer": answer, "results": hits}
