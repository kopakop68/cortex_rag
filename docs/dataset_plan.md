# Dataset Plan — Cortex RAG

## Sources
1) MITRE ATT&CK (enterprise JSON)
2) Sigma Rules (SigmaHQ/sigma)
3) YARA samples (optional)
4) Sample SIEM alerts (Elastic/Splunk examples)

**Focus (v1):**
- Platforms: Windows + Cloud (AWS/Azure) first
- Tactics priority: Credential Access, Execution, Discovery, Exfiltration

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
  "severity": "low|medium|high (optional)",
  "log_source": "EDR|Sysmon|CloudTrail|AAD|Defender (optional)",
  "created_at": "iso8601",
  "extra": {}
}

## ETL Steps
- Load → Normalize → Chunk → Save JSONL in `data/processed/`
- Extract ATT&CK `technique_id` even if nested under `external_references`
- Preserve headings/bullets where possible for better chunk boundaries

## Validation
- Ensure required fields: `id`, `doc_type`, `text`, `source`
- If present, validate `technique_id` shape (e.g., T1059, T1003.*)

## Gold Set
- `/eval/gold_questions.jsonl` with representative questions (triage/rules/explain/mitigate)

