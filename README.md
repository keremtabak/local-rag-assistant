# 🤖 Local RAG Assistant

A fully local Retrieval-Augmented Generation (RAG) assistant built with Python, SQLite, Sentence Transformers, Microsoft Foundry Local, Phi-4 Mini, and Streamlit.

The application allows users to upload PDF, DOCX, and TXT documents, perform semantic search on document content, and receive AI-generated answers powered by a local language model.

---

## 🚀 Features

✅ PDF Upload

✅ DOCX Upload

✅ TXT Upload

✅ Automatic Document Processing

✅ Text Chunking

✅ SQLite Storage

✅ Embedding Generation

✅ Semantic Search

✅ Cosine Similarity Search

✅ Top-K Retrieval

✅ Context Generation

✅ Microsoft Foundry Local

✅ Phi-4 Mini Integration

✅ Streamlit Web Interface

✅ Fully Local Execution

---

## 🏗 Architecture

```text
Document Upload
       ↓
   Text Extraction
       ↓
     Chunking
       ↓
      SQLite
       ↓
    Embeddings
       ↓
 Semantic Search
       ↓
 Top-K Retrieval
       ↓
     Context
       ↓
   RAG Prompt
       ↓
    Phi-4 Mini
       ↓
      Answer
```

## 🛠 Tech Stack

- Python
- Streamlit
- SQLite
- Sentence Transformers
- scikit-learn
- Microsoft Foundry Local
- Phi-4 Mini

---

## 📂 Project Structure

```text
local-rag-assistant/
│
├── app.py
├── rag.py
├── ingest.py
├── database.py
├── requirements.txt
└── README.md
```

---

## 📄 Supported File Types

- PDF
- DOCX
- TXT

---

## 🔍 How It Works

1. Upload a document.
2. Extract text from the document.
3. Split text into chunks.
4. Store chunks in SQLite.
5. Generate embeddings.
6. Perform semantic search.
7. Retrieve the most relevant chunks.
8. Build a RAG prompt.
9. Send the prompt to Phi-4 Mini.
10. Generate an answer.

---

## 🖥 Demo

### Upload Document

Upload a PDF, DOCX, or TXT file directly from the web interface.

### Ask Questions

Example:

```text
What is this document about?
```

### View Retrieved Context

The application can display the retrieved context used to generate the answer.

---

## 🎯 Roadmap

### v1.1

- Chat history
- Source citations

### v1.2

- Multi-document support
- Better retrieval ranking

### v1.3

- FAISS / ChromaDB integration
- Streaming responses

### v2.0

- FastAPI backend
- Docker deployment
- Authentication
- Production-ready architecture

---

## 📷 Screenshots

Add screenshots here after deployment.

Example:

images/main-screen.png

images/question-answering.png

---

## 👨‍💻 Author

Muhammet Kerem Tabak

GitHub:
https://github.com/keremtabak