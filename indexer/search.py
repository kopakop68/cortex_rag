# indexer/search.py
import argparse, json, pathlib, sys
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
INDEX_DIR = PROJECT_ROOT / "data" / "faiss"
PROC_DIR = PROJECT_ROOT / "data" / "processed"
META_PATH = INDEX_DIR / "meta.jsonl"
INDEX_PATH = INDEX_DIR / "index.faiss"
MODEL_PATH = INDEX_DIR / "model.txt"

def load_meta():
    rows = []
    with META_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows

def load_texts():
    # Load original texts to print snippets
    texts = []
    for name in ["attack_normalized.jsonl", "sigma_normalized.jsonl"]:
        p = PROC_DIR / name
        if not p.exists():
            continue
        with p.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rec = json.loads(line)
                    texts.append(rec.get("text",""))
    return texts

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", required=True, help="Query text")
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--min-score", type=float, default=0.0, help="Filter out results below this cosine score")
    ap.add_argument("--doc-type", choices=["attack","sigma","yara","siem","any"], default="any")
    ap.add_argument("--json", action="store_true", help="Print JSON array instead of pretty text")
    ap.add_argument("--show-text", action="store_true", help="Show a short text snippet for each hit")
    args = ap.parse_args()

    # Basic guardrails
    if not INDEX_PATH.exists() or not META_PATH.exists() or not MODEL_PATH.exists():
        print("Index or metadata missing. Run: python indexer/embed.py", file=sys.stderr)
        sys.exit(2)

    model_name = MODEL_PATH.read_text().strip()
    model = SentenceTransformer(model_name)
    index = faiss.read_index(str(INDEX_PATH))
    meta = load_meta()

    # Optional full texts for snippets
    texts = load_texts() if args.show_text else None

    qvec = model.encode([args.q], normalize_embeddings=True)
    qvec = np.asarray(qvec, dtype="float32")
    D, I = index.search(qvec, args.k * 5)  # overfetch, then post-filter

    results = []
    for idx, score in zip(I[0], D[0]):
        if idx < 0:  # FAISS may return -1 if not enough entries
            continue
        m = meta[idx]
        if args.doc_type != "any" and m.get("doc_type") != args.doc_type:
            continue
        if score < args.min_score:
            continue

        item = {
            "rank": len(results) + 1,
            "score": float(score),
            "doc_type": m.get("doc_type"),
            "title": m.get("title"),
            "technique_id": m.get("technique_id"),
            "source": m.get("source"),
            "index": int(idx),
        }
        if texts is not None and idx < len(texts):
            t = texts[idx]
            # small snippet
            item["snippet"] = (t[:280] + "…") if len(t) > 280 else t
        results.append(item)
        if len(results) >= args.k:
            break

    if args.json:
        print(json.dumps({"query": args.q, "results": results}, ensure_ascii=False, indent=2))
    else:
        print(f"\nTop-{args.k} for: {args.q}\n")
        for r in results:
            tid = f" [{r['technique_id']}]" if r.get("technique_id") else ""
            print(f"{r['rank']}. score={r['score']:.4f}  [{r['doc_type']}] {r.get('title','')}{tid}")
            print(f"   source: {r.get('source')}")
            if args.show_text and r.get("snippet"):
                print(f"   text: {r['snippet']}")
            print()

if __name__ == "__main__":
    main()
