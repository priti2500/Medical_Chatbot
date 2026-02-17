"""
Data ingestion: load medical content from files and split into chunks for embedding.
Supports JSON (e.g. FAQs) and plain text.
"""
import json
import logging
from pathlib import Path
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from config.settings import DATA_RAW

logger = logging.getLogger(__name__)

# Chunk size tuned for embedding models (e.g. OpenAI) and retrieval quality
CHUNK_SIZE = 400
CHUNK_OVERLAP = 50


def load_faq_json(path: Path) -> List[Document]:
    """
    Load a JSON file with FAQ entries: list of {question, answer, category?}.
    Each entry becomes one or more Document chunks.
    """
    docs = []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        data = [data]
    for item in data:
        q = item.get("question", "")
        a = item.get("answer", "")
        cat = item.get("category", "general")
        text = f"Q: {q}\nA: {a}\nCategory: {cat}"
        docs.append(Document(page_content=text, metadata={"source": str(path), "category": cat}))
    return docs


def load_text_file(path: Path) -> List[Document]:
    """Load a plain text file and return as a single Document (to be split later)."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return [Document(page_content=text, metadata={"source": str(path)})]


def load_all_raw_data(data_dir: Path | None = None) -> List[Document]:
    """
    Load all supported files from data/raw.
    Returns a list of LangChain Documents (may be large; split in next step).
    """
    data_dir = data_dir or DATA_RAW
    if not data_dir.exists():
        logger.warning("Data directory does not exist: %s", data_dir)
        return []
    documents = []
    for path in data_dir.iterdir():
        if path.suffix.lower() == ".json":
            try:
                documents.extend(load_faq_json(path))
            except Exception as e:
                logger.exception("Failed to load %s: %s", path, e)
        elif path.suffix.lower() in (".txt", ".md"):
            try:
                documents.extend(load_text_file(path))
            except Exception as e:
                logger.exception("Failed to load %s: %s", path, e)
    logger.info("Loaded %d document(s) from %s", len(documents), data_dir)
    return documents


def split_documents(documents: List[Document]) -> List[Document]:
    """
    Split documents into smaller chunks for embedding.
    Uses RecursiveCharacterTextSplitter to keep sentences intact when possible.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    logger.info("Split into %d chunks", len(chunks))
    return chunks
