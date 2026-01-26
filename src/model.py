from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from src.config import (
    MODEL_PATH, 
    CONTEXT_WINDOW, 
    MAX_NEW_TOKENS, 
    TEMPERATURE,
    EMBEDDING_MODEL_NAME,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)

def init_settings():
    """Initialize global settings for LlamaIndex."""
    
    # Initialize LLM
    llm = LlamaCPP(
        model_path=MODEL_PATH,
        temperature=TEMPERATURE,
        max_new_tokens=MAX_NEW_TOKENS,
        context_window=CONTEXT_WINDOW,
        generate_kwargs={},
        model_kwargs={"n_gpu_layers": -1}, # Use all GPU layers if available
        verbose=True
    )
    
    # Initialize Embedding Model
    embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL_NAME)
    
    # Configure global settings
    Settings.llm = llm
    Settings.embed_model = embed_model
    Settings.context_window = CONTEXT_WINDOW
    Settings.num_output = MAX_NEW_TOKENS
    Settings.chunk_size = CHUNK_SIZE
    Settings.chunk_overlap = CHUNK_OVERLAP
    
    return llm, embed_model
