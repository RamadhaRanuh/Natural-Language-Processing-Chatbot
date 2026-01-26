import os
from llama_index.core import (
    VectorStoreIndex, 
    SimpleDirectoryReader, 
    StorageContext, 
    load_index_from_storage
)
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from src.config import DATA_DIR, STORAGE_DIR
from src.model import init_settings

def build_index():
    """Load documents and build/save the index."""
    
    # Initialize settings (LLM & Embeddings)
    init_settings()
    
    # Check if storage directory exists
    if not os.path.exists(STORAGE_DIR):
        print("Creating new index...")
        
        # Load documents
        print(f"Loading documents from {DATA_DIR}...")
        documents = SimpleDirectoryReader(DATA_DIR).load_data()
        print(f"Loaded {len(documents)} documents.")
        
        # Initialize Vector Store (ChromaDB)
        db = chromadb.PersistentClient(path=os.path.join(STORAGE_DIR, "chroma_db"))
        chroma_collection = db.get_or_create_collection("medical_docs")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        # Create Index
        index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context, show_progress=True
        )
        
        # Persist index (metadata mainly, as vector store is already persistent)
        index.storage_context.persist(persist_dir=STORAGE_DIR)
        print("Index created and saved.")
        return index
    else:
        print("Index already exists. Loading...")
        
        # Load Vector Store
        db = chromadb.PersistentClient(path=os.path.join(STORAGE_DIR, "chroma_db"))
        chroma_collection = db.get_or_create_collection("medical_docs")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store, persist_dir=STORAGE_DIR)
        
        # Load Index
        index = load_index_from_storage(storage_context)
        print("Index loaded.")
        return index

if __name__ == "__main__":
    build_index()
