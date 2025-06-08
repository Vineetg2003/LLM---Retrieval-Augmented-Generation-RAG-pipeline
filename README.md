# 📄 RAG-Powered PDF Question Answering System

## 🧠 Overview

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline that allows users to:

- 📤 Upload PDF documents  
- ❓ Ask questions based on their content  
- 💬 Get accurate, context-aware answers from an LLM  

The system leverages:

- 🧠 FAISS for fast vector search  
- 🧬 Sentence Transformers for embeddings  
- 🤖 A transformer-based LLM (`flan-t5-base`) for answer generation  
- 🐳 Docker for easy deployment  

---

## 🔗 Live Demo

[Click here to view the demo](https://drive.google.com/file/d/12DdhZ9Npyastx-NuH73bAoCxmT7pVYEj/view?usp=sharing)

## 🖼️ Frontend Screenshot

![Frontend UI Screenshot](RAGIMAGE.png)

---

## 🚀 Frontend Deployment Link
You can access the frontend deployment at:
https://vineetg2003-llm---retrieval-augmented-genera-frontendapp-sqpnux.streamlit.app/

- Note:
**This frontend link fetches data from your local PC backend. So you must run the backend server on http://localhost:8000 simultaneously using the command below for the frontend to work properly:**

```bash
uvicorn app.main:app --reload
```

---

## ⚙️ Features

✅ PDF Upload with chunking + OCR fallback  
✅ Semantic retrieval with FAISS  
✅ Context-aware responses using `flan-t5-base`  
✅ FastAPI-based backend  
✅ Dockerized setup for portability  

---

## 🛠️ Tech Stack

| Layer             | Tool/Library                            |
|------------------|-----------------------------------------|
| Backend API      | FastAPI                                 |
| PDF Processing   | PyPDF2, pdf2image, pytesseract          |
| Embedding        | `all-MiniLM-L6-v2` (Sentence Transformers) |
| Vector Store     | FAISS                                   |
| LLM              | `google/flan-t5-base` (Transformers)    |
| Frontend         | Streamlit                               |
| Containerization | Docker + Docker Compose                 |

---

## 🧠 Model Selection

**We use the google/flan-t5-base model for answer generation. This is a lightweight transformer-based language model from the FLAN-T5 family, designed to balance speed and accuracy. It performs well on small to medium-scale tasks and fits comfortably within 8GB RAM, which suits our development system.**

**Due to hardware constraints, especially limited memory and no dedicated GPU, chunking is capped at 512 tokens, and retrieval size is optimized for efficiency. While this setup is sufficient for most use cases, it may not handle long or highly complex PDFs well.**

**For users with more powerful hardware (≥16GB RAM and GPU), larger models like Mistral-7B-Instruct can be integrated for significantly better performance and deeper contextual understanding.**

---

## 📦 Installation

### 🔧 Prerequisites

- Python 3.9+
- Git
- Docker & Docker Compose
- Poppler & Tesseract (for OCR)

#### 🐧 Ubuntu / Window Setup

```bash
sudo apt update
sudo apt install -y poppler-utils tesseract-ocr

# Clone the repo
git clone https://github.com/Vineetg2003/LLM---Retrieval-Augmented-Generation-RAG-pipeline.git
cd RAG-APP

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
cd .\backend\
huggingface-cli login

Testing Token generated from official website of Hugging Face

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn main:app --reload --port 8000

# OR Run with Docker
docker-compose up --build

.
rag-app/
│
├── backend/
│   ├── api/                     # FastAPI routes
│   │   ├── routes.py
│   ├── core/                    # Embedding & LLM logic
│   │   ├── chunker.py
│   │   ├── embedder.py
│   │   ├── retriever.py
│   │   ├── llm.py
│   ├── db/
│   │   ├── metadata_store.py    # Simple SQLite/Mongo metadata
│   ├── main.py                  # FastAPI entrypoint
│   ├── utils.py
│   └── requirements.txt
│   └── Dockerfile.backend
│
├── frontend/
│   ├── app.py                   # Streamlit frontend
│   └── requirements.txt
│   └── Dockerfile.frontend
│
├── docker-compose.yml
├── tests/
│   └── test_pipeline.py         # Unit tests
└── README.md


```

## 📈 Performance Note

💻 Developed and tested on a system with **8GB RAM**.  
We use `flan-t5-base` (small and efficient).  
For better performance:

- Use `flan-t5-large` or `mistral-7b-instruct` (requires more RAM/GPU)  
- Tune chunk sizes and model max token limits accordingly

---
## 🧪 Testing

- Unit tests cover PDF chunking, vector store indexing, and query handling.
- Integration tests validate end-to-end upload and question-answer workflows.
- Run tests using:

```bash
pytest tests/

```

---

## ⚙️ Configuring Different LLM Providers

The system uses google/flan-t5-base by default.
To switch models, update the MODEL_NAME variable in llm.py:
MODEL_NAME = "your-chosen-llm-model"

---

## 📤 API Usage Guide

### ▶️ Upload a PDF

**Endpoint**: `POST /api/upload/`  
**Content-Type**: `multipart/form-data` with a `.pdf` file  

**Example using curl:**

```bash
curl -X POST "http://localhost:8000/api/upload/" \
  -H "accept: application/json" \
  -F "file=@yourfile.pdf"
```

### ❓ Query the Uploaded Content

**Endpoint**: `POST /api/query/`  
**Content-Type**: `application/json`  
**Request Body**:

```json
{
  "question": "What is the project deadline mentioned in the PDF?"
}

*Example using curl:*
curl -X POST "http://localhost:8000/api/query/" \
  -H "Content-Type: application/json" \
  -d '{"question":"What is the project deadline mentioned in the PDF?"}'

*Response:*
{
  "answer": "The project deadline is June 30, 2025."
}

```

---

## 🐳 Docker Setup & Deployment Guide

This section walks you through setting up and running the entire system using Docker and Docker Compose for easy deployment.

---

### 1. **Prerequisites**

- Install [Docker](https://docs.docker.com/get-docker/) on your machine  
- Install [Docker Compose](https://docs.docker.com/compose/install/) (usually bundled with Docker Desktop)  

Verify installation:

```bash
docker --version
docker-compose --version

```