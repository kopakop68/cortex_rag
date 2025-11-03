# api/llm.py
import os
from groq import Groq

def get_groq_client():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise RuntimeError("GROQ_API_KEY missing in environment (.env)")
    return Groq(api_key=key)

def chat_once(system_prompt: str, user_prompt: str, model: str | None = None, max_tokens: int = 800):
    client = get_groq_client()
    model = model or os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content
