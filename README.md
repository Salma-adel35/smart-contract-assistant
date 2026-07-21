# Smart Contract AI Assistant

## RAG-Based Contract Question Answering and LLM-Based Evaluation

Smart Contract AI Assistant is an intelligent document question-answering application that allows users to upload PDF and DOCX contracts, ask questions in natural language, and receive answers grounded in the uploaded documents.

The application uses a Retrieval-Augmented Generation (RAG) architecture to retrieve relevant contract sections before generating an answer. It also provides source snippets for transparency and includes an LLM-as-a-Judge evaluation module to assess the quality of generated answers.

The application supports questions in both English and Arabic.

---

## Project Overview

Legal and business contracts often contain large amounts of complex information. Finding specific clauses manually can be time-consuming and difficult.

This project provides an AI-powered assistant that enables users to:

* Upload one or multiple contracts
* Ask natural-language questions about the uploaded documents
* Retrieve relevant sections from the contracts
* Generate context-aware answers using a Large Language Model
* Display the sources used to generate the answer
* Maintain a ChatGPT-style conversation history
* Evaluate generated answers using an LLM-based judge

The system is designed to reduce the time required to search and understand information inside contract documents.

---

## Features

### Document Upload

The application supports:

* PDF files
* DOCX files
* Multiple documents at the same time

When documents are uploaded, they are automatically processed and indexed.

---

### Document Processing

The document processing pipeline includes:

1. File parsing
2. Text extraction
3. Document chunking
4. Embedding generation
5. Vector store creation

This prepares the uploaded contracts for semantic retrieval.

---

### Retrieval-Augmented Generation (RAG)

The application uses a RAG pipeline to ground the generated answers in the uploaded documents.

Instead of asking the LLM to answer from its general knowledge, the system:

1. Receives the user's question
2. Searches the vector store for relevant document chunks
3. Retrieves the most relevant context
4. Sends the question and retrieved context to the LLM
5. Generates an answer based on the retrieved contract content

This helps reduce unsupported or hallucinated answers.

---

### Source Citations

For every generated answer, the application displays relevant source snippets from the uploaded documents.

This allows users to:

* Verify the generated answer
* Identify the original contract section
* Understand where the answer came from

---

### ChatGPT-Style Interface

The application provides a conversational interface that includes:

* User questions
* Assistant answers
* Source snippets
* Persistent chat history
* Clear chat functionality

Users can ask multiple questions about the uploaded contracts in the same session.

---

### LLM-as-a-Judge Evaluation

The project includes an automated evaluation module.

Users can evaluate a generated answer using a dedicated evaluation button.

The judge LLM evaluates the answer based on:

* Accuracy
* Relevance
* Grounding in the retrieved sources

The evaluation returns:

```text
Verdict: Correct / Incorrect
Score: 0–100
Explanation: Short reasoning behind the evaluation
```

The evaluation module is implemented separately from the main RAG pipeline to maintain a modular architecture.

---

# System Architecture

```text
                    ┌──────────────────────┐
                    │       User           │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Streamlit UI       │
                    │  Upload + Questions  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Document Ingestion   │
                    │ PDF / DOCX Parsing   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Chunking        │
                    │ Recursive Splitter   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Embeddings       │
                    │ SentenceTransformers │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     FAISS Vector     │
                    │       Store          │
                    └──────────┬───────────┘
                               │
                      User Question
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Semantic Retrieval   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Groq LLM        │
                    │   Answer Generation  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Answer + Sources     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ LLM-as-a-Judge       │
                    │ Evaluation Module    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Verdict + Score +    │
                    │ Explanation          │
                    └──────────────────────┘
```

---

# RAG Pipeline

The RAG pipeline consists of the following stages:

## 1. Document Ingestion

Uploaded files are processed according to their file type.

### PDF

PDF text is extracted using PyMuPDF.

### DOCX

Text is extracted using the `python-docx` library.

The extracted text is converted into LangChain `Document` objects with metadata such as the original filename.

---

## 2. Text Chunking

Large documents are divided into smaller chunks using:

```text
RecursiveCharacterTextSplitter
```

The current configuration uses:

```text
chunk_size = 800
chunk_overlap = 150
```

### Why Chunking?

Large documents cannot always be passed to the LLM as one complete context.

Chunking:

* Reduces the amount of text processed at once
* Improves retrieval performance
* Helps retrieve only relevant sections
* Makes embedding generation more efficient

### Why Chunk Overlap?

The overlap helps preserve context between neighboring chunks.

Without overlap, important information located at the boundary between two chunks could be separated.

---

## 3. Embeddings

Each document chunk is converted into a numerical vector representation called an embedding.

Embeddings represent the semantic meaning of the text.

For example:

```text
"How can the agreement be terminated?"
```

and:

```text
"Either party may terminate this agreement by providing written notice."
```

may have similar vector representations even though they do not contain the exact same words.

---

## 4. FAISS Vector Store

The generated embeddings are stored in a FAISS vector store.

FAISS enables efficient similarity search over the document embeddings.

When the user asks a question:

1. The question is converted into an embedding
2. The vector store compares it with document chunk embeddings
3. The most semantically relevant chunks are retrieved

---

## 5. Answer Generation

The retrieved document chunks are passed as context to the Groq-powered LLM.

The LLM uses:

* The user's question
* The retrieved contract context

to generate a grounded answer.

The answer is then displayed together with the relevant source snippets.

---

# Evaluation Module

The project includes an independent LLM-as-a-Judge evaluation component.

The evaluation process works as follows:

```text
User Question
      │
      ▼
Generated Answer
      │
      ▼
Retrieved Sources
      │
      ▼
Judge LLM
      │
      ▼
Evaluation Result
      │
      ├── Verdict
      ├── Score
      └── Explanation
```

The judge evaluates whether the generated answer:

* Correctly answers the question
* Is supported by the retrieved sources
* Avoids unsupported information

The evaluation result contains:

```text
{
    "verdict": "Correct",
    "score": 90,
    "explanation": "The answer is supported by the retrieved contract section."
}
```

The evaluation module is separated from the RAG generation pipeline so that answer generation and answer evaluation remain independent components.

---

# Project Structure

```text
smart_contract_assistant/
│
├── app.py
│
├── ingestion/
│   ├── parser.py
│   └── splitter.py
│
├── retrieval/
│   ├── vectorstore.py
│   └── rag_chain.py
│
├── evaluation/
│   └── judge.py
│
├── utils/
│   └── helpers.py
│
├── requirements.txt
│
├── .gitignore
│
└── .env
```

---

# Technologies Used

| Technology           | Purpose                          |
| -------------------- | -------------------------------- |
| Python               | Core programming language        |
| Streamlit            | Web application interface        |
| LangChain            | LLM and RAG pipeline integration |
| Groq API             | LLM inference                    |
| FAISS                | Vector similarity search         |
| SentenceTransformers | Text embeddings                  |
| PyMuPDF              | PDF text extraction              |
| python-docx          | DOCX text extraction             |
| python-dotenv        | Environment variable management  |

---

# Installation

## 1. Clone the Repository

```bash
git clone <your-repository-url>
cd smart_contract_assistant
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

The `.env` file should never be committed to GitHub.

Make sure it is included in `.gitignore:

```text
.env
venv/
__pycache__/
*.pyc
```

---

# Running the Application

Run:

```bash
streamlit run app.py
```

The application will open in the browser.

---

# Example Usage

### Step 1

Upload one or more PDF or DOCX contracts.

### Step 2

The system automatically:

* Extracts the text
* Splits the text into chunks
* Generates embeddings
* Builds the FAISS vector store

### Step 3

Ask a question such as:

```text
What is the termination clause in the contract?
```

### Step 4

The assistant retrieves the relevant contract sections and generates an answer.

### Step 5

The application displays:

* The generated answer
* Source snippets
* The original document name

### Step 6

The user can click the evaluation button to evaluate the generated answer.

---

# Example Output

```text
Question:
What is the termination clause in the contract?

Answer:
The agreement may be terminated by providing written notice to the other party according to the terms specified in the contract.

Sources:
Contract.pdf
Relevant contract snippet...

Evaluation:
Verdict: Correct
Score: 92/100
Explanation:
The answer is consistent with the retrieved contract content.
```

---

# Design Decisions

## Why RAG?

RAG allows the system to answer questions based on the uploaded contracts instead of relying only on the LLM's pre-trained knowledge.

This is especially important for legal documents because answers should be grounded in the actual contract content.

---

## Why FAISS?

FAISS was selected because it:

* Provides efficient vector similarity search
* Works well with embeddings
* Is lightweight and easy to integrate
* Is suitable for local development and prototyping

---

## Why SentenceTransformers?

SentenceTransformers provides semantic embeddings that represent the meaning of text.

This allows the system to retrieve relevant content even when the question and contract use different wording.

---

## Why Groq?

Groq provides fast LLM inference and can be integrated with LangChain to generate responses efficiently.

---

## Why LangChain?

LangChain simplifies the integration of:

* LLMs
* Prompts
* Document objects
* Retrievers
* Vector stores
* RAG chains

It also helps organize the application into modular components.

---

# Security Considerations

API keys are stored in environment variables rather than hardcoded in the source code.

The `.env` file is excluded from version control using `.gitignore`.

Sensitive API keys should never be uploaded to GitHub.

---

# Limitations

The current version has several limitations:

* The vector store is created during the application session
* The system depends on the availability of the LLM API
* The quality of the answer depends on the quality of document extraction and retrieval
* Scanned PDFs may require OCR before text can be extracted
* LLM-based evaluation is not a perfect replacement for human evaluation

---

# Future Improvements

Possible future improvements include:

* OCR support for scanned contracts
* Persistent vector databases
* Streaming LLM responses
* Advanced contract summarization
* Clause extraction
* Contract comparison
* Risk detection
* User authentication
* Database integration
* Cloud deployment
* More advanced evaluation metrics
* Hybrid keyword and semantic search
* Reranking retrieved documents

---

# Learning Outcomes

Through this project, I gained practical experience in:

* Retrieval-Augmented Generation
* Large Language Model integration
* Prompt engineering
* Vector databases
* Semantic search
* Document processing
* Embeddings
* LangChain
* Groq API integration
* Streamlit application development
* LLM-based evaluation
* Modular software architecture
* API key security
* Debugging and deployment preparation

---

# Acknowledgment

This project was developed as the final project for an ITI training program.

The project provided practical experience in designing and implementing an end-to-end AI application that combines document processing, semantic retrieval, Large Language Models, and automated evaluation.

---

# Author

Developed by Salma Adel.

This project demonstrates an end-to-end implementation of an AI-powered Smart Contract Assistant using RAG and LLM-based evaluation.
