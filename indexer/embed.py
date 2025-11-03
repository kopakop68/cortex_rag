# indexer/embed.py
import json, pathlib, argparse
from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
PROC_DIR = PROJECT_ROOT / "data" / "processed"
INDEX_DIR = PROJECT_ROOT / "data" / "faiss"
INDEX_DIR.mkdir(parents=True, exist_ok=True)

META_PATH = INDEX_DIR / "meta.jsonl"
INDEX_PATH = INDEX_DIR / "index.faiss"
MODEL_PATH = INDEX_DIR / "model.txt"

def load_jsonl(path: pathlib.Path) -> List[Dict[str, Any]]:
    rows = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

def write_jsonl(path: pathlib.Path, rows: List[Dict[str, Any]]):
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def build_index(model_name: str, batch_size: int = 128):
    # 1) load processed records
    records: List[Dict[str, Any]] = []
    for name in ["attack_normalized.jsonl", "sigma_normalized.jsonl"]:
        records += load_jsonl(PROC_DIR / name)
    print(f"[EMBED] Total records to index: {len(records)}")
    if not records:
        print("[EMBED] Nothing to index. Exiting.")
        return

    # 2) texts + metadata
    texts = [r["text"] for r in records]
    meta = [
        {
            "id": r.get("id"),
            "title": r.get("title"),
            "doc_type": r.get("doc_type"),
            "source": r.get("source"),
            "tactic": r.get("tactic"),
            "technique_id": r.get("technique_id"),
            "platform": r.get("platform"),
        }
        for r in records
    ]

    # 3) embeddings
    print(f"[EMBED] Loading model: {model_name}")
    model = SentenceTransformer(model_name)
    vecs = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        normalize_embeddings=True,   # use cosine via inner product
    )
    vecs = np.asarray(vecs, dtype="float32")
    dim = vecs.shape[1]
    print(f"[EMBED] Embedding shape: {vecs.shape}")

    # 4) FAISS index (Inner Product with normalized vectors = cosine)
    index = faiss.IndexFlatIP(dim)
    index.add(vecs)
    faiss.write_index(index, str(INDEX_PATH))
    write_jsonl(META_PATH, meta)
    MODEL_PATH.write_text(model_name)

    print(f"[EMBED] Saved index → {INDEX_PATH}")
    print(f"[EMBED] Saved metadata → {META_PATH}")
    print(f"[EMBED] Saved model name → {MODEL_PATH}")
    print("[EMBED] Done.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="sentence-transformers/all-mpnet-base-v2")
    ap.add_argument("--batch-size", type=int, default=128)
    args = ap.parse_args()
    build_index(args.model, args.batch_size)

if __name__ == "__main__":
    main()
