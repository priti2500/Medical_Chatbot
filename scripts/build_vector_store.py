"""
Build the vector store from data in data/raw/.
Run once after adding/changing medical content, and before starting the chatbot.

Usage:
    python scripts/build_vector_store.py
"""
import sys
from pathlib import Path

# Ensure project root is on path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils import setup_logging
from src.embeddings import build_faiss_index


def main():
    setup_logging()
    print("Loading data from data/raw/ and building FAISS index (HuggingFace embeddings)...")
    build_faiss_index()
    print("Done. Vector store saved to vector_store/faiss_index")


if __name__ == "__main__":
    main()
