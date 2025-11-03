# ingest/etl_attack_sigma.py
from __future__ import annotations
import json, uuid, os, pathlib, datetime
from typing import Dict, Any, Iterable, List

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROC_DIR = PROJECT_ROOT / "data" / "processed"
PROC_DIR.mkdir(parents=True, exist_ok=True)

def now_iso() -> str:
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def normalize_attack(attack_obj: Dict[str, Any]):
    for item in attack_obj.get("objects", []):
        text = item.get("description") or ""
        if not text.strip():
            continue
        technique = None
        for ref in item.get("external_references", []):
            if ref.get("external_id", "").startswith("T"):
                technique = ref["external_id"]; break
        yield {
            "id": str(uuid.uuid4()),
            "doc_type": "attack",
            "title": item.get("name") or "ATT&CK Item",
            "text": text,
            "source": "attack_enterprise.json",
            "tactic": None,
            "technique_id": technique,
            "platform": None,
            "detection": None,
            "mitigation": None,
            "created_at": now_iso(),
            "extra": {"type": item.get("type")}
        }

def normalize_sigma(rule_texts: List[str]):
    for i, raw in enumerate(rule_texts):
        yield {
            "id": str(uuid.uuid4()),
            "doc_type": "sigma",
            "title": f"Sigma Rule {i+1}",
            "text": raw[:4000],
            "source": "sigma_repo",
            "tactic": None,
            "technique_id": None,
            "platform": None,
            "detection": None,
            "mitigation": None,
            "created_at": now_iso(),
            "extra": {}
        }

def write_jsonl(path: pathlib.Path, records):
    with path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def main():
    print("[ETL] Starting…")
    attack_path = RAW_DIR / "attack_enterprise.json"
    if attack_path.exists():
        with attack_path.open("r", encoding="utf-8") as f:
            attack_obj = json.load(f)
        recs = list(normalize_attack(attack_obj))
        write_jsonl(PROC_DIR / "attack_normalized.jsonl", recs)
        print(f"[ETL] ATT&CK normalized: {len(recs)}")
    else:
        print("[ETL] Skipping ATT&CK — not found:", attack_path)

    sigma_recs = list(normalize_sigma(["example sigma rule yaml text"]))
    write_jsonl(PROC_DIR / "sigma_normalized.jsonl", sigma_recs)
    print(f"[ETL] Sigma normalized: {len(sigma_recs)}")
    print("[ETL] Done.")

if __name__ == "__main__":
    main()
