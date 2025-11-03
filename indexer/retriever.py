import json, pathlib
from typing import List, Dict, Any
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
INDEX_DIR = PROJECT_ROOT / "data" / "faiss"
PROC_DIR = PROJECT_ROOT / "data" / "processed"

META_PATH = INDEX_DIR / "meta.jsonl"
INDEX_PATH = INDEX_DIR / "index.faiss"
MODEL_PATH = INDEX_DIR / "model.txt"

class Retriever:
    def __init__(self):
        if not INDEX_PATH.exists() or not META_PATH.exists() or not MODEL_PATH.exists():
            raise RuntimeError("Index not built. Run: python indexer/embed.py")
        self.model_name = MODEL_PATH.read_text().strip()
        self.model = SentenceTransformer(self.model_name)
        self.index = faiss.read_index(str(INDEX_PATH))
        self.meta = self._load_jsonl(META_PATH)
        self.texts = self._load_texts()

    def _load_jsonl(self, path: pathlib.Path) -> List[Dict[str, Any]]:
        rows = []
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rows.append(json.loads(line))
        return rows

    def _load_texts(self) -> List[str]:
        texts = []
        for name in ["attack_normalized.jsonl", "sigma_normalized.jsonl"]:
            p = PROC_DIR / name
            if p.exists():
                with p.open("r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            rec = json.loads(line)
                            texts.append(rec.get("text", ""))
        return texts

    def search(self, q: str, k: int = 5, min_score: float = 0.0, doc_type: str = "any"):
        qvec = self.model.encode([q], normalize_embeddings=True)
        qvec = np.asarray(qvec, dtype="float32")
        D, I = self.index.search(qvec, k * 5)  # overfetch, then filter

        out = []
        for idx, score in zip(I[0], D[0]):
            if idx < 0:
                continue
            m = self.meta[idx]
            if doc_type != "any" and m.get("doc_type") != doc_type:
                continue
            if score < min_score:
                continue
            item = {
                "score": float(score),
                "doc_type": m.get("doc_type"),
                "title": m.get("title"),
                "technique_id": m.get("technique_id"),
                "source": m.get("source"),
                "index": int(idx),
                "snippet": (self.texts[idx][:280] + "…") if idx < len(self.texts) and len(self.texts[idx]) > 280 else self.texts[idx],
            }
            out.append(item)
            if len(out) >= k:
                break
        return out
