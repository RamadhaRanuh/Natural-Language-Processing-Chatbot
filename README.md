# Personal-Chatbot_LLM_RAG

### Download the Model: zephyr-7b-beta.Q5_K_M.gguf
### From the following link: [https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/tree/main](https://huggingface.co/TheBloke/zephyr-7B-beta-GGUF)

---

This project implements an AI chatbot using Large Language Models (LLM) and Retrieval Augmented Generation (RAG) techniques to provide detailed answers based on knowledge extracted from PDF documents.

## Features

- **LLM Integration**: Utilizes LlamaCPP for seamless integration with the LlamaCore C++ library, supporting both CPU and GPU acceleration for enhanced performance.
  
- **RAG Technique**: Implements Retrieval Augmented Generation to combine generative models with information retrieval from PDF documents, improving answer accuracy and relevance.
  
- **PDF Document Knowledge**: Uses llama_index for efficient handling and extraction of information from PDF documents, ensuring comprehensive responses.

## Requirements

- Python 3.10.*
- LlamaCPP (supports both CPU and GPU)
- llama_index
- Hugging Face Transformers (for LLM models)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your_username/your_repo.git
   cd your_repo
   ```

2. Install `llama-cpp-python` by following the instructions [here](https://github.com/abetlen/llama-cpp-python).

3. Install additional dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up LlamaCPP and download necessary models following the provided instructions.

## Usage

1. Run the python script:
   ```
   python Main.py
   ```

2. Interact with the chatbot to ask questions related to PDF documents and observe its responses.

## Examples

- Query the chatbot with various questions about the content of PDF documents to test its knowledge retrieval capabilities.
- Explore different configurations and parameters to optimize performance and response quality.
