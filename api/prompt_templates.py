# api/prompt_templates.py

SYSTEM_PROMPT = """You are a Security Copilot.
Answer ONLY using the provided context. If context is insufficient or irrelevant, reply:
"Insufficient context to answer reliably."
Always include citations using [source:TYPE][technique:TID] when available.
Be concise, structured, and practical for SOC/DFIR workflows."""

def format_context(chunks, max_chars_per_chunk=800):
    lines = []
    for i, c in enumerate(chunks, start=1):
        title = c.get("title") or ""
        doc_type = c.get("doc_type") or ""
        tid = c.get("technique_id") or ""
        src = c.get("source") or ""
        snip = (c.get("snippet") or "")[:max_chars_per_chunk]
        head = f"[{i}] ({doc_type}) {title}"
        if tid: head += f" [{tid}]"
        if src: head += f" <{src}>"
        lines.append(head + "\n" + snip)
    return "\n\n".join(lines)

USER_TEMPLATE = """Question:
{question}

Context (use ONLY this information):
{context}

Requirements:
- Start with a 2–3 line summary.
- If applicable, list ATT&CK techniques as bullets: "TID — short name".
- Provide practical detections/mitigations if relevant.
- End with citations like: [source:attack][technique:T1003], [source:sigma].
- If context is weak, say: "Insufficient context to answer reliably."
"""

def build_user_prompt(question: str, chunks):
    ctx = format_context(chunks)
    return USER_TEMPLATE.format(question=question, context=ctx)
