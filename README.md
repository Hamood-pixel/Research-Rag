<div align="center">
  <h1>📄 Research Paper AI Assistant</h1>
  <h3>A Privacy-First, 100% Local RAG Engine Running on Your GPU</h3>
  <p><i>Automated text ingestion, vectorized chunking, and context-anchored inference.</i></p>

  <p>
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
    <img src="https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white" alt="Ollama" />
    <img src="https://img.shields.io/badge/LangChain-1C3C3A?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain" />
  </p>
</div>

<hr />

<h2>🏗️ System Architecture</h2>
<p>The pipeline uses a modern, decoupled asynchronous microservices setup designed to keep your private data completely isolated on your machine:</p>

<pre align="left">
┌─────────────────────────┐                    ┌────────────────────────┐
│  Frontend: Streamlit    │──(HTTP POST Req)──►│    Backend: FastAPI    │
└─────────────────────────┘                    └────────────────────────┘
             │                                              │
             ▼                                              ▼
 📁 Document Ingestion System                  🧠 Intelligent Query System
 [PyPDFLoader] ➔ [RecursiveSplitter]           [Vector Similarity Search via ChromaDB]
             │                                              │
             ▼                                              ▼
 🛡️ Embedding Engine (Local GPU)               🤖 Local LLM Execution Engine
 [sentence-transformers/all-MiniLM-L6-v2]      [Ollama: Llama3]
             │                                              │
             ▼                                              ▼
 💾 Persistent Vector Vault                    📥 Deterministic Context
 [ChromaDB] ◄────────────────────────────────── Custom Prompt Constraint
</pre>

---

## ✨ System Highlights

* 🔒 **100% Local Privacy:** Zero data leaves your machine. No API keys, no corporate telemetry, and no hidden data scraping.
* ⚡ **Async File Ingestion:** Leverages FastAPI's asynchronous background loops to allow smooth, non-blocking binary file uploads.
* 📑 **Metadata-Preserving Chunking:** Uses smart recursive character parsing to loop through papers layout-by-layout, maintaining page numbers and references intact.
* 🎯 **Anti-Hallucination Guardrails:** Employs strict semantic prompt boundaries to force the LLM to anchor its answers *only* within the extracted context blocks.

---

## 🛠️ Tech Stack & Hardware Mapping

<table>
  <tr>
    <th>Layer</th>
    <th>Technology</th>
    <th>Hardware Utilization / Function</th>
  </tr>
  <tr>
    <td><b>Frontend UI</b></td>
    <td>Streamlit Dashboard</td>
    <td>Handles user drag-and-drop actions and structures conversational message blocks.</td>
  </tr>
  <tr>
    <td><b>Application Gateway</b></td>
    <td>FastAPI / Uvicorn</td>
    <td>Orchestrates endpoint routing, asynchronous payload reading, and multi-part form streaming.</td>
  </tr>
  <tr>
    <td><b>Embedding Processor</b></td>
    <td>all-MiniLM-L6-v2 (HF)</td>
    <td>Runs locally to transform raw text blocks into dense 384-dimensional mathematical coordinates.</td>
  </tr>
  <tr>
    <td><b>Vector Database</b></td>
    <td>ChromaDB Vector Vault</td>
    <td>Handles ultra-fast Cosine/L2 distance calculations for matching queries with data on disk.</td>
  </tr>
  <tr>
    <td><b>Inference Brain</b></td>
    <td>Ollama (Llama3)</td>
    <td>Compiles deep-learning contextual responses directly using local <b>GPU hardware</b>.</td>
  </tr>
</table>

---

## 📁 Repository Blueprint

```text
research-rag/
│
├── backend/
│   ├── uploads/            # Temporary disk buffers for uploaded file bytes
│   ├── chroma_db/          # SQLite binary storage housing the persistent vector embeddings
│   ├── main.py             # FastAPI control center and endpoint definitions
│   ├── processor.py        # PDF text parsing & chunk segmentation architecture
│   └── db.py               # ChromaDB client initialization and search operations
│
└── frontend/
    └── app.py              # Streamlit state configurations and connection routines
```
# 🚀 Installation & Dual-Terminal Execution
1. Initialize Backend Model
Ensure Ollama is booted on your local system, and fetch your preferred open-weights LLM:

``` ollama run llama3 ```

2. Environment Setup

Clone this codebase, isolate your dependencies inside a virtual environment, and pull down the packages:

```
# Establish virtual environment
python -m venv venv

# Activate execution policies & trigger state change on Windows PowerShell
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& ".\venv\Scripts\Activate.ps1")

# Populate dependencies
pip install fastapi uvicorn streamlit langchain langchain-community langchain-text-splitters langchain-ollama sentence-transformers chromadb python-multipart requests
```

3. Launching the Platform

This environment runs a decoupled client-server architecture, which means you need to launch two separate terminals inside VS Code:
```
python backend/main.py
Expected output line: INFO: Uvicorn running on http://0.0.0.0:8000

streamlit run frontend/app.py
Expected output line: Local URL: http://localhost:8501
```

# 🛡️ Operational Safety Defenses

SSD Wear Protection: Wrapped completely in a strict try...finally block. Source files are completely shredded from your storage drives the instant they are safely converted to vectors.

Memory Protection: Utilizes direct binary stream chunk buffers via python-multipart to keep system RAM lean and fast, even when ingesting huge, multi-page research documents.
