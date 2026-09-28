# Medical Retrieval Chatbot (OpenEvidence Style)

This project is a high-performance **Medical Retrieval-Augmented Generation (RAG)** chatbot designed to answer complex medical questions using local trusted medical literature (e.g., *Gale Encyclopedia of Medicine*). 

It features a modern, premium **client-server architecture**:
- **Backend API**: Built with **FastAPI** & **LlamaIndex** for efficient retrieval and streaming response generation.
- **Frontend UI**: Built with **Next.js**, **Tailwind CSS**, and **React Markdown** to mimic the "OpenEvidence" look and feel.

## Features

- **Local RAG Pipeline**: Uses `llama-index` and local vector stores (`ChromaDB`) to retrieve relevant context from indexed PDF documents.
- **Streaming Responses**: Real-time token streaming for a responsive user experience.
- **Premium UI**: 
    - "OpenEvidence" inspired design with an orange theme.
    - Markdown rendering for rich text answers.
    - Responsive layout (Desktop Sidebar + Mobile Header).
    - Floating input bar and clean typography.
- **Local Inference**: Supports local GGUF models (e.g., Qwen, Zephyr) via `llama-cpp-python`.

## Architecture

- **Backend (`src/`)**: Python/FastAPI
    - `src/api.py`: REST API endpoints (streaming chat).
    - `src/rag.py`: RAG logic and query engine setup.
    - `src/ingest.py`: Document ingestion script.
- **Frontend (`frontend/`)**: TypeScript/Next.js
    - `src/app/page.tsx`: Main chat interface.
    - `src/app/globals.css`: Global styling (Tailwind).

## Requirements

- **Python 3.10+**
- **Node.js 18+** & **npm**
- **Hardware**: Sufficient RAM/VRAM to run the local LLM (e.g., 8GB+ RAM).

## Installation

### 1. Backend Setup

1.  **Clone the repository** and navigate to the root directory.
2.  **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Download the Model**:
    Ensure the GGUF model (e.g., `Qwen3-4B-Instruct-2507-Q5_K_S-4.74bpw.gguf`) is placed in the project root or configured in `src/config.py`.
4.  **Ingest Data** (Run once to build index):
    ```bash
    python src/ingest.py
    ```

### 2. Frontend Setup

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  **Install Node dependencies**:
    ```bash
    npm install
    ```

## Usage

You need to run both the backend and frontend servers simultaneously.

### Terminal 1: Application Backend
Start the FastAPI streaming server:
```bash
# From the project root
python -m src.api
```
*Server running at http://localhost:8000*

### Terminal 2: Application Frontend
Start the Next.js development server:
```bash
# From the frontend/ directory
npm run dev
```
*UI running at http://localhost:3000*

Open your browser and navigate to **[http://localhost:3000](http://localhost:3000)** to start using the chatbot.
