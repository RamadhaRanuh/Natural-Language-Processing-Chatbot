import os
import chromadb
from llama_index.core import StorageContext, load_index_from_storage, get_response_synthesizer
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import Settings
from src.config import STORAGE_DIR, SIMILARITY_TOP_K
from src.model import init_settings

def get_query_engine():
    """Load index and create query engine."""
    
    # specific settings.
    init_settings()
        
        
    print("Loading index for RAG pipeline...")
    
    # Load Vector Store
    db = chromadb.PersistentClient(path=os.path.join(STORAGE_DIR, "chroma_db"))
    chroma_collection = db.get_or_create_collection("medical_docs")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store, persist_dir=STORAGE_DIR)
    
    # Load Index
    index = load_index_from_storage(storage_context)
    
    # Configure Retriever
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=SIMILARITY_TOP_K,
    )
    
    # Configure Response Synthesizer
    response_synthesizer = get_response_synthesizer(
        response_mode="compact",
        streaming=True,
    )
    
    # Create Query Engine
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
    )
    
    print("Query engine ready.")
    return query_engine
