# indexer/embed.py
import json, pathlib
from typing import List, Dict, Any

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
PROC_DIR = PROJECT_ROOT / "data" / "processed"

def load_jsonl(path: pathlib.Path) -> List[Dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

def main():
    records = []
    for name in ["attack_normalized.jsonl", "sigma_normalized.jsonl"]:
        p = PROC_DIR / name
        if p.exists():
            records.extend(load_jsonl(p))
    print(f"[EMBED] Total records available: {len(records)}")
    print("[EMBED] TODO: generate embeddings and build FAISS index.")

if __name__ == "__main__":
    main()
