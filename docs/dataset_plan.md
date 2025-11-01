# Dataset Plan — Cortex RAG

## Sources
1) MITRE ATT&CK (enterprise JSON)  
2) Sigma Rules (SigmaHQ/sigma)  
3) YARA samples (optional)  
4) Sample SIEM alerts (Elastic/Splunk examples)

## Normalized Schema (per chunk)
{
  "id": "uuid",
  "doc_type": "attack|sigma|yara|siem",
  "title": "string",
  "text": "chunked text",
  "source": "path-or-url",
  "tactic": "TA000x (optional)",
  "technique_id": "Txxxx (optional)",
  "platform": "windows|linux|mac|cloud (optional)",
  "detection": "string (optional)",
  "mitigation": "string (optional)",
  "created_at": "iso8601",
  "extra": { }
}

## ETL Steps
Load → Normalize → Chunk → Save JSONL in `data/processed/`

## Validation
Ensure fields exist; keep ATT&CK technique ids when present.

## Gold Set
/eval/gold_questions.jsonl with representative security questions.
