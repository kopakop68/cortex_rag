#!/usr/bin/env python3
import json
from pathlib import Path

events_path = Path("data/events.jsonl")
out = Path("reports/day6_report.md")

lines = []

lines.append("# Day 6 — Evaluation Report\n")

latencies = []
scores = []
tokens = 0
n = 0

for line in events_path.read_text().splitlines():
    o = json.loads(line)
    latencies.append(o["latency"])
    tokens += o["tokens"]
    n += 1

if n == 0:
    raise SystemExit("no events found")

lines.append(f"- total questions: {n}")
lines.append(f"- avg latency: {sum(latencies)/n:.2f}s")
lines.append(f"- avg tokens: {tokens//n}")
lines.append("")

lines.append("## Next actions")
lines.append("- add more data (Sigma/YARA)")
lines.append("- try smaller model for faster response")
lines.append("- also test different top-k values")

out.write_text("\n".join(lines))
print("✓ wrote", out)
print("--- Preview ---")
print("\n".join(lines))
