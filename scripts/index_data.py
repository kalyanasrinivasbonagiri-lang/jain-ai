import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from jain_ai.rag.pipeline import get_rag_pipeline


if __name__ == "__main__":
    pipeline = get_rag_pipeline()
    pipeline.initialize()
    print("Index initialization completed.")
