import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from jain_ai.rag.indexing import initialize_vector_resources, reset_vector_store


if __name__ == "__main__":
    print("Resetting vector store and processed file tracker...")
    reset_vector_store()
    print("Rebuilding embeddings and Chroma vector DB from all source documents...")
    initialize_vector_resources()
    print("Reindex completed.")
