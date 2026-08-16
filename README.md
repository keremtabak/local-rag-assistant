# 🤖 Local RAG Assistant

A fully local Retrieval-Augmented Generation (RAG) assistant built with Python, SQLite, Sentence Transformers, Microsoft Foundry Local, Phi-4 Mini, and Streamlit.

This application allows users to upload PDF, DOCX, and TXT documents, perform semantic search on document content, and receive AI-generated answers powered entirely by a locally running language model.

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

✅ Microsoft Foundry Local Integration

✅ Phi-4 Mini Integration

✅ Streamlit Web Interface

✅ Fully Local Execution

✅ Context Inspection

✅ Retrieval-Augmented Generation (RAG)

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

---

## 🛠 Tech Stack

- Python
- Streamlit
- SQLite
- Sentence Transformers
- scikit-learn
- Microsoft Foundry Local
- Phi-4 Mini
- Hugging Face Models

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
├── README.md
└── .gitignore
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
3. Split the text into chunks.
4. Store chunks in SQLite.
5. Generate embeddings.
6. Perform semantic search.
7. Retrieve the most relevant chunks.
8. Build a RAG prompt.
9. Send the prompt to Phi-4 Mini.
10. Generate an answer.

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/keremtabak/local-rag-assistant.git
```

Navigate to the project directory:

```bash
cd local-rag-assistant
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run

Start the Streamlit application:

```bash
streamlit run app.py
```

Application URL:

```text
http://localhost:8501
```

---

## 🧠 AI Models

This project uses:

- Microsoft Foundry Local
- Phi-4 Mini
- Sentence Transformers (all-MiniLM-L6-v2)

The entire pipeline runs locally on the user's machine.

No cloud-based LLM is required.

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

## 🎬 Demo Workflow

```text
Upload PDF / DOCX / TXT
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
      Phi-4 Mini
          ↓
       Answer
```

---

## 📷 Screenshots

### Main Application

Place a screenshot of the main interface here.

```text
images/main-screen.png
```

### Document Upload

Place a screenshot of the document upload workflow here.

```text
images/upload-screen.png
```

### Question Answering

Place a screenshot showing question answering and retrieved context.

```text
images/question-answering.png
```

---

## 🎯 Roadmap

### v1.1

- Chat History
- Source Citations
- Better Prompt Engineering

### v1.2

- Multi-Document Support
- Better Retrieval Ranking
- Document Management

### v1.3

- FAISS Integration
- ChromaDB Integration
- Streaming Responses

### v2.0

- FastAPI Backend
- Docker Support
- Authentication
- Production Architecture
- Conversation Memory

---

## 👨‍💻 Author

**Muhammet Kerem Tabak**

GitHub:

https://github.com/keremtabak

---

## ⭐ Project Goal

Build a fully local AI assistant capable of answering questions from user-provided documents using Retrieval-Augmented Generation (RAG), Semantic Search, and Microsoft Foundry Local.