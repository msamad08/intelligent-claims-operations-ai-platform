# Intelligent Claims & Operations AI Platform

Enterprise Retrieval-Augmented Generation (RAG) platform for insurance claims intelligence, SOP retrieval, incident response guidance, and operational decision support.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-brightgreen)](https://intelligent-claims-operations-ai-platform.onrender.com)


## Platform Preview

### Conversational RAG Interface

![RAG Assistant](outputs/figures/rag_chat_interface.png)

### FastAPI Backend

![Swagger UI](outputs/figures/swagger_ui.png)

### System Architecture

![Architecture Diagram](outputs/figures/architecture_diagram.png)
---

## Live Features

* Conversational AI assistant interface
* PDF upload and ingestion workflow
* Semantic document retrieval
* Vector database search using ChromaDB
* Local embedding models using SentenceTransformers
* Local LLM summarization using Ollama and Llama 3.2
* Cost-free local RAG response generation
* Claims intelligence workflows
* Operational SOP retrieval
* Incident response guidance
* Confidence scoring and escalation logic
* FastAPI backend service
* Streamlit conversational frontend
* Docker deployment support

---

## System Architecture

```text
PDF Documents
      â†“
Document Ingestion Pipeline
      â†“
Text Chunking
      â†“
SentenceTransformer Embeddings
      â†“
Chroma Vector Database
      â†“
Semantic Retrieval Engine
      â†“
Operational Intelligence Layer
      â†“
Confidence Scoring + Escalation Logic
      â†“
FastAPI Backend
      â†“
Streamlit Conversational Interface
```

---

## Core Technologies

### AI / Machine Learning

* Python
* LangChain
* SentenceTransformers
* ChromaDB
* Semantic Retrieval
* Retrieval-Augmented Generation (RAG)
* Vector Search
* HuggingFace Embeddings
* Ollama / Llama 3.2
* OpenAI GPT-3.5 Turbo

### Backend / APIs

* FastAPI
* Uvicorn
* REST API Architecture

### Frontend / Visualization

* Streamlit
* Conversational Chat Interface

### Data Engineering

* PDF Ingestion Pipelines
* Text Chunking
* Document Parsing
* Vector Database Workflows

### Deployment

* Docker
* Render
* GitHub

---

## Project Structure

```text
intelligent-claims-operations-ai-platform/
â”‚
â”œâ”€â”€ data/
â”‚   â”œâ”€â”€ documents/
â”‚   â””â”€â”€ processed/
â”‚
â”œâ”€â”€ outputs/
â”‚   â”œâ”€â”€ figures/
â”‚   â””â”€â”€ reports/
â”‚
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ app.py
â”‚   â”œâ”€â”€ api.py
â”‚   â”œâ”€â”€ ingest_documents.py
â”‚   â”œâ”€â”€ rag_pipeline.py
â”‚   â””â”€â”€ guardrails.py
â”‚
â”œâ”€â”€ vectorstore/
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ Dockerfile
â”œâ”€â”€ start.sh
â”œâ”€â”€ .env.example
â”œâ”€â”€ .gitignore
â””â”€â”€ README.md
```

---
## Ollama Setup (Local Only)

Required if running locally without an OpenAI API key.

Install Ollama from [https://ollama.com](https://ollama.com)

Then pull and serve the model:

```bash
ollama pull llama3.2
ollama serve
```

---
## Environment Configuration

Copy `.env.example` to `.env` before running:

#### Windows PowerShell

```powershell
Copy-Item ".env.example" ".env"
```

#### macOS / Linux

```bash
cp .env.example .env
```

Then open `.env` and fill in your values:

```env
# Option 1: OpenAI (cloud deployment)
OPENAI_API_KEY=your-openai-key-here

# Option 2: Local Ollama (leave OPENAI_API_KEY blank)
OLLAMA_HOST=http://localhost:11434
```

> The app automatically uses OpenAI if `OPENAI_API_KEY` is set, otherwise falls back to Ollama.

---
## Quickstart

1. Complete Ollama setup above (local) or set `OPENAI_API_KEY` in `.env` (cloud)
2. Clone the repo and install dependencies
3. Place PDF documents into `data/documents/`
4. Run ingestion:
```bash
python src/ingest_documents.py
```
5. Start the app:
```bash
python -m streamlit run src/app.py
```

---

## Local Installation

### Clone Repository

```bash
git clone https://github.com/msamad08/intelligent-claims-operations-ai-platform.git
cd intelligent-claims-operations-ai-platform
```

### Create Virtual Environment

```bash
python -m venv .venv
```
### Activate Environment

#### Windows PowerShell

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

#### macOS / Linux

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Streamlit Application

```bash
python -m streamlit run src/app.py
```

Then open:
http://localhost:8501

---

## Running the FastAPI Backend

```bash
python -m uvicorn src.api:app --reload
```

Swagger UI:
http://127.0.0.1:8000/docs

---

## PDF Ingestion Workflow

Place PDF documents into:
data/documents/

Then run:

```bash
python src/ingest_documents.py
```

This pipeline:

* Loads PDFs
* Splits documents into chunks
* Generates embeddings
* Builds the vector database
* Enables semantic retrieval

---

## Docker Deployment

### Build Docker Image

```bash
docker build -t intelligent-claims-ai .
```

### Run Docker Container

```bash
docker run -p 8501:8501 -p 8000:8000 intelligent-claims-ai
```

> **Note:** Ollama must be running on your host machine before starting the container.
> The container connects to it via `host.docker.internal:11434`.
> For cloud deployment, set `OPENAI_API_KEY` as an environment variable instead.

---

## Example Questions
What documentation is required during insurance claims processing?

What operational steps should be taken during severe storm incidents?

When should claims be escalated to a supervisor?

What information must be documented before emergency mitigation begins?

---

## Example Enterprise Workflow

1. User uploads claims policy documents
2. Documents are chunked and embedded
3. ChromaDB stores semantic vectors
4. User submits operational question
5. Semantic retrieval finds relevant sections
6. AI assistant generates grounded response
7. Confidence scoring and escalation logic applied
8. Sources returned to user

---

## Future Enhancements

Planned future improvements include:

* Authentication and role-based access
* Citation highlighting
* Multi-document reasoning
* Hybrid BM25 + vector retrieval
* CI/CD automation
* Conversation memory
* Agentic workflow orchestration
* Operational analytics dashboard integration

---

## Strategic Portfolio Value

This project demonstrates:

* Enterprise GenAI architecture
* Retrieval-Augmented Generation (RAG)
* Vector database engineering
* Semantic retrieval systems
* FastAPI backend deployment
* Streamlit frontend engineering
* Operational AI workflows
* Decision-support system design
* Claims intelligence automation
* AI-driven document intelligence

---

## Author

Mohammad Samad
Data Scientist | AI & Operational Intelligence | Predictive Analytics | Operations Research

GitHub: [https://github.com/msamad08]

