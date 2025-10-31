import streamlit as st
import requests

st.set_page_config(page_title="Cortex RAG", layout="wide")

st.title("🧠 Cortex RAG — Security Copilot")
st.write("Ask natural-language questions grounded in ATT&CK, Sigma/YARA, and SIEM alerts.")

q = st.text_input("Your question")
if st.button("Ask") and q:
    try:
        resp = requests.post("http://localhost:8000/ask", json={"question": q}, timeout=30)
        data = resp.json()
        st.subheader("Answer")
        st.write(data.get("answer"))
        st.subheader("Citations")
        st.write(data.get("citations"))
    except Exception as e:
        st.error(f"API error: {e}")
