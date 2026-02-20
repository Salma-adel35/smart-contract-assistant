Smart Contract AI Assistant
RAG-Based Contract Q&A + Automated LLM Evaluation

Overview
Smart Contract AI Assistant is an intelligent Retrieval-Augmented Generation (RAG) system that allows users to:

Upload PDF and DOCX contracts

Ask natural language questions

Receive grounded answers using RAG

Automatically evaluate answer quality

Interact via a ChatGPT-style interface

This project demonstrates real-world large language model (LLM) integration with structured evaluation and a modular architecture.

Architecture
User
  │
  ▼
Streamlit Chat UI
  │
  ▼
RAG Pipeline
  ├── Document Parsing
  ├── Chunking
  ├── Embeddings
  ├── Vector Store
  └── Retriever
  │
  ▼
Groq LLM (Answer Generation)
  │
  ▼
Evaluation Module (Groq Judge)
  │
  ▼
Verdict + Score + Explanation
Core Features
Multi-Document Upload
Supports PDF and DOCX files

Multiple files can be uploaded simultaneously

Automatic re-indexing when files are updated

Retrieval-Augmented Generation (RAG)
Document parsing and chunk splitting

Embedding generation

Vector database storage

Context-aware answer generation

Ensures answers are grounded in the contract content

ChatGPT-Style Interface
Questions appear as chat messages

Latest answers displayed first

Persistent chat history

Clear conversational layout with a “Clear Chat” button

Automated Answer Evaluation
Evaluates each response using an LLM-based judge

Criteria include:

Accuracy

Source grounding

Logical consistency

Returns structured output:

Verdict: Correct / Incorrect

Score: 0–100

Explanation: Short reasoning

Project Structure
smart_contract_assistant/
│
├── app.py
├── ingestion/
│   ├── parser.py
│   └── splitter.py
├── retrieval/
│   ├── vectorstore.py
│   └── rag_chain.py
├── evaluation/
│   └── judge.py
├── utils/
│   └── helpers.py
└── .env
Tech Stack
Python

Streamlit

LangChain

Groq API

Vector Store (FAISS or similar)

RAG Architecture

Regex-based Structured Output Parsing

Environment Setup
Clone Repository

git clone https://github.com/your-username/smart-contract-assistant.git
cd smart-contract-assistant
Create Virtual Environment

python -m venv venv
venv\Scripts\activate   # Windows
Install Dependencies

pip install -r requirements.txt
Add Environment Variables

Create .env file:

GROQ_API_KEY=your_groq_api_key_here
Run the App
streamlit run app.py
Then open in your browser:
http://localhost:8501

How It Works
User uploads contracts

System parses and splits documents

Chunks are embedded and stored

User asks a question

Retriever fetches relevant context

Groq LLM generates grounded answer

Judge LLM evaluates the answer

Verdict, score, and explanation are returned

Why This Project Is Strong
Real-world RAG implementation

Modular and clean architecture

LLM-based automatic evaluation

Structured output handling

Chat-style UI

Production-ready logic

Robust error handling

Future Improvements
Streaming token responses

Asynchronous LLM calls

Fine-tuned contract evaluation model

User authentication

Cloud deployment (AWS / GCP / Azure)

UI theming & dark mode

Evaluation confidence scoring

Skills Demonstrated
LLM Integration

Retrieval-Augmented Generation

Prompt Engineering

Structured Output Handling

Modular Backend Design

Streamlit Frontend Development

API Integration

Error Handling & Debugging

Author
Developed as an AI-powered Smart Contract Assistant integrating RAG and automated LLM evaluation.
