# ui/app.py
import streamlit as st
import requests
import json
from typing import List, Dict

API_URL = "http://127.0.0.1:8000/ask"  # make sure FastAPI is running on this URL/port

st.set_page_config(page_title="Cortex RAG — Chat", layout="wide")

st.title("Cortex RAG — Security Copilot")
st.write("Ask security questions and get RAG-grounded answers (ATT&CK, Sigma, YARA, SIEM).")

with st.sidebar:
    st.header("Settings")
    k = st.slider("Number of context chunks (k)", min_value=1, max_value=10, value=5)
    doc_type = st.selectbox("Doc type", options=["any", "attack", "sigma", "yara", "siem"], index=0)

if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Ask a question", placeholder="e.g. How to detect credential dumping on Windows?")
if st.button("Ask") and query.strip():
    payload = {"question": query, "k": k, "doc_type": doc_type}
    with st.spinner("Querying Cortex RAG…"):
        try:
            r = requests.post(API_URL, json=payload, timeout=60)
            r.raise_for_status()
            resp = r.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
            resp = None

    if resp:
        answer = resp.get("answer") or "No answer returned."
        results = resp.get("results", [])

        st.session_state.history.insert(0, {"q": query, "answer": answer, "results": results})

# show latest response first
for item in st.session_state.history:
    st.markdown("---")
    st.markdown(f"**Q:** {item['q']}")
    st.markdown("**Answer:**")
    st.code(item["answer"], language="text")

    if item["results"]:
        with st.expander(f"Show {len(item['results'])} retrieved chunks (for citations)"):
            for i, r in enumerate(item["results"], start=1):
                score = r.get("score")
                title = r.get("title") or ""
                doc_type = r.get("doc_type") or ""
                source = r.get("source") or ""
                tid = r.get("technique_id") or ""
                snippet = r.get("snippet") or ""
                st.markdown(f"**{i}. [{doc_type}] {title}**  — score: {score:.3f}")
                if tid:
                    st.markdown(f"- **Technique:** {tid}")
                st.markdown(f"- **Source:** `{source}`")
                st.write(snippet)
