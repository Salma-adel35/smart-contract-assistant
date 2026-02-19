# Smart Contract Summary & Q&A Assistant

**Domain:** LLM Pipelines, LangChain, Vector Stores, Gradio, LangServe  
**Type:** Workshop Application Project (NVIDIA DLI Course Alignment)

## Project Overview
This project is a web application that allows users to upload PDF or DOCX contracts and interact with them using a smart assistant powered by large language models (LLMs).  
It supports question answering with **source citations** for every answer.

---

## Features
- Upload PDF/DOCX contracts
- Extract text from documents
- Chunk documents for processing
- Generate embeddings and store them in a FAISS vector store
- Retrieval-Augmented Generation (RAG) for question answering
- Display source snippets for each answer
- Track session state in the app (uploaded documents, QA history)
- Simple and clean UI using Streamlit

### Optional Features (Not Required)
- Summarization of uploaded contracts
- Evaluation metrics for QA performance
- Ability to answer general questions without uploading files

---

## Installation

1. Clone the repo:

```bash
git clone <your-repo-url>
cd smart-contract-assistant

