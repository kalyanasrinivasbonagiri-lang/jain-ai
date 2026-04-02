import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from jain_ai.config import RAW_DATA_DIR, VECTOR_DB_DIR


if __name__ == "__main__":
    print("RAW_DATA_DIR:", RAW_DATA_DIR)
    print("VECTOR_DB_DIR:", VECTOR_DB_DIR)
    print("PDF count:", len([name for name in os.listdir(RAW_DATA_DIR) if name.lower().endswith(".pdf")]))
