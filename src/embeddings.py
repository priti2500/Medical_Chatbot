"""
Embedding generation and vector store management.

Uses HuggingFace SentenceTransformers embeddings
(`sentence-transformers/all-MiniLM-L6-v2`) with a local FAISS index.
No OpenAI or other external embedding API is required.
"""
import logging
from pathlib import Path
from typing import List

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from config.settings import VECTOR_STORE_PATH
from src.ingest import load_all_raw_data, split_documents

logger = logging.getLogger(__name__)

EMBEDDING_TYPE_FILE = "embedding_type.txt"

# HuggingFace model name corresponding to your “AL-MINI-L6”
HF_EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def get_embeddings():
    """
    Return HuggingFace SentenceTransformers embeddings.

    This uses a local model from HuggingFace Hub and does not require any
    API key. If you have a GPU, you can change `device` to "cuda".
    """
    return HuggingFaceEmbeddings(
        model_name=HF_EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"},
    )


def build_faiss_index(
    documents: List[Document] | None = None,
    persist_path: Path | None = None,
) -> FAISS:
    """
    Build a FAISS index from documents. If documents not provided,
    load from data/raw.

    Saves index to persist_path (default from settings).
    Uses local HuggingFace embeddings only (no external API).
    """
    persist_path = persist_path or VECTOR_STORE_PATH
    persist_path = Path(persist_path)
    persist_path.mkdir(parents=True, exist_ok=True)

    if documents is None:
        raw_docs = load_all_raw_data()
        documents = split_documents(raw_docs)
    if not documents:
        raise ValueError("No documents to index. Add files to data/raw/ and run again.")

    embeddings = get_embeddings()
    vector_store = FAISS.from_documents(documents, embeddings)
    vector_store.save_local(str(persist_path))

    # Remember which embeddings we used so load can use the same
    (persist_path / EMBEDDING_TYPE_FILE).write_text(
        "local_hf",
        encoding="utf-8",
    )
    logger.info(
        "FAISS index saved to %s (embeddings: %s)",
        persist_path,
        HF_EMBEDDING_MODEL_NAME,
    )
    return vector_store


def load_faiss_index(persist_path: Path | None = None) -> FAISS:
    """
    Load an existing FAISS index from disk.
    Always uses the same HuggingFace embeddings as when the index was built.
    """
    persist_path = persist_path or VECTOR_STORE_PATH
    persist_path = Path(persist_path)
    if not persist_path.exists():
        raise FileNotFoundError(
            f"Vector store not found at {persist_path}. "
            "Run: python scripts/build_vector_store.py"
        )

    embeddings = get_embeddings()
    return FAISS.load_local(str(persist_path), embeddings, allow_dangerous_deserialization=True)
