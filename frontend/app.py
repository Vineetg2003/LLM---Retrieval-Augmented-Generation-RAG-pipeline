import streamlit as st
from utils import upload_pdf, query_llm

st.set_page_config(page_title="RAG Assistant", layout="centered")

# 🔶 Highlighted Notice
st.warning("⚠️ This frontend link fetches data from your local PC backend. So you must run the backend server on http://localhost:8000 simultaneously using the command below for the frontend to work properly:\n\n```bash\nuvicorn main:app --reload --port 8000\n```")

st.title("📄 Retrieval-Augmented Generation (RAG) Assistant")

# Upload Section
st.header("Upload Documents")
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Uploading and indexing..."):
        result = upload_pdf(uploaded_file)
    st.success(result.get("message", "Uploaded successfully."))

# Query Section
st.header("Ask a Question")
query = st.text_input("Type your question:")

if st.button("Get Answer") and query:
    with st.spinner("Thinking..."):
        result = query_llm(query)
    st.markdown("### 💬 Answer")
    st.write(result.get("answer", "No answer returned."))
