import os
import streamlit as st
from dotenv import load_dotenv
from ingestion.parser import parse_files
from ingestion.splitter import split_documents
from retrieval.vectorstore import build_vectorstore
from retrieval.rag_chain import build_rag_chain
from utils.helpers import format_sources


from evaluation.judge import evaluate_answer as evaluate_answer_auto


load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


st.set_page_config(page_title="Smart Contract Assistant", page_icon="📜")
st.title("📜 Smart Contract Summary & Q&A Assistant")


for key in ["vectorstore", "rag_chain", "retriever", "current_files", "chat_history"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "chat_history" and key != "current_files" else []


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
            rag_chain, retriever = build_rag_chain(vectorstore, GROQ_API_KEY)

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


query_col, _ = st.columns([8, 2])
query = query_col.text_input("Type your question here:")

ask_button = st.button("Ask")

if ask_button and query:
    if st.session_state.rag_chain is None:
        st.warning("Upload at least one document first.")
    else:
        with st.spinner("Thinking..."):
            answer = st.session_state.rag_chain.invoke(query)
            docs = st.session_state.retriever.invoke(query)
            sources_formatted = format_sources(docs)

        
        st.session_state.chat_history.insert(0, {
            "question": query,
            "answer": answer,
            "sources": sources_formatted,
            "evaluation": None  
        })


if st.session_state.chat_history:
    st.markdown("## 💬 Chat History")
    for idx, chat in enumerate(st.session_state.chat_history):
        with st.chat_message("user"):
            st.write(chat["question"])
        with st.chat_message("assistant"):
            st.write(chat["answer"])
            st.markdown("**Sources:**")
            st.write(chat["sources"])

        
        if st.button(f"Evaluate Answer ✅", key=f"eval_{idx}"):
            try:
                evaluation_result = evaluate_answer_auto(
                    question=chat["question"],
                    answer=chat["answer"],
                    sources=chat["sources"]
                )
                chat["evaluation"] = evaluation_result
                st.success("Evaluation done!")
            except Exception as e:
                chat["evaluation"] = {"verdict": "Error", "score": 0, "explanation": str(e)}
                st.error(f"Evaluation failed: {e}")

        
        if chat.get("evaluation"):
            st.markdown("### 🏆 Evaluation")
            st.write(f"**Verdict:** {chat['evaluation'].get('verdict', 'Error')}")
            st.write(f"**Score:** {chat['evaluation'].get('score', 0)}/100")
            explanation = chat['evaluation'].get('explanation')
            if explanation:
                st.markdown(f"**Explanation:** {explanation}")


if st.button("🗑 Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()
