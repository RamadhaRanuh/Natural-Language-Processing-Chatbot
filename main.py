from src.ui import launch_ui
from src.ingest import build_index
import os
from src.config import STORAGE_DIR

def main():
    print("Starting Medical Retrieval Chatbot...")
    
    # Check if index exists, if not build it
    if not os.path.exists(STORAGE_DIR):
        print("Index not found. Starting ingestion process...")
        build_index()
    else:
        print("Index found.")
        
    # Launch UI
    print("Launching Interface...")
    launch_ui()

if __name__ == "__main__":
    main()
