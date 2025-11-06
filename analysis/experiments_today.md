# Day 6 — Experiments

We are going to test multiple settings to see if we can reduce latency while keeping answer quality.

## Baseline (already measured)
- model: llama-3.1-8b-instant
- top-k: 5
- avg latency: ~2.53s
- tokens: ~676
- quality: acceptable

---

## Experiment 1 — try top-k = 3

Command:

```bash
curl -s -X POST http://127.0.0.1:8000/ask \
  -H 'Content-Type: application/json' \
  -d '{"question":"How to detect credential dumping on Windows?","k":3}' | jq .

## Experiment 2 — top-k = 2
- latency: 2.53 s
- tokens: 676
- quality note: good, slightly verbose

## Experiment 3 — top-k = 3
- latency: 1.55 s
- tokens: 503
- quality note: concise, still complete (best trade-off)

