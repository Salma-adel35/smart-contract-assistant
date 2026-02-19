import os
import streamlit as st
from dotenv import load_dotenv

from ingestion.parser import parse_files
from ingestion.splitter import split_documents
from retrieval.vectorstore import build_vectorstore
from retrieval.rag_chain import build_rag_chain
from utils.helpers import format_sources

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="Smart Contract Assistant", page_icon="📜")
st.title("📜 Smart Contract Summary & Q&A Assistant")

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "current_files" not in st.session_state:
    st.session_state.current_files = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_files = st.file_uploader(
    "Upload PDF or DOCX contracts",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

current_file_names = [f.name for f in uploaded_files] if uploaded_files else []

if current_file_names != st.session_state.current_files:

    if uploaded_files:
        with st.spinner("Processing documents..."):

            docs = parse_files(uploaded_files)
            chunks = split_documents(docs)
            vectorstore = build_vectorstore(chunks)

            rag_chain, retriever = build_rag_chain(vectorstore, groq_api_key)

            st.session_state.vectorstore = vectorstore
            st.session_state.rag_chain = rag_chain
            st.session_state.retriever = retriever

        st.success("Documents indexed successfully ✅")

    else:
        st.session_state.vectorstore = None
        st.session_state.rag_chain = None
        st.session_state.retriever = None
        st.info("All documents removed.")

    st.session_state.current_files = current_file_names

query = st.text_input("Ask a question about the uploaded contracts:")

if st.button("Ask") and query:

    if st.session_state.rag_chain is None:
        st.warning("Upload at least one document first.")
    else:
        with st.spinner("Thinking..."):
            answer = st.session_state.rag_chain.invoke(query)
            docs = st.session_state.retriever.invoke(query)

        
        st.session_state.chat_history.append({
            "question": query,
            "answer": answer,
            "sources": format_sources(docs)
        })



if st.session_state.chat_history:

    st.markdown("## 💬 Chat History")

    for chat in st.session_state.chat_history:

        with st.chat_message("user"):
            st.write(chat["question"])

        with st.chat_message("assistant"):
            st.write(chat["answer"])
            st.markdown("**Sources:**")
            st.write(chat["sources"])

   
    if st.button("🗑 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()
