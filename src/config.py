import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "Dataset")
STORAGE_DIR = os.path.join(BASE_DIR, "storage")
MODEL_PATH = os.path.join(BASE_DIR, "Qwen3-4B-Instruct-2507-Q5_K_S-4.74bpw.gguf")

# Model Settings
CONTEXT_WINDOW = 4096
MAX_NEW_TOKENS = 512
TEMPERATURE = 0.2

# Embedding Model
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"

# RAG Settings
SIMILARITY_TOP_K = 2
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50
