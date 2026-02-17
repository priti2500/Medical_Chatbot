"""
Tests for data ingestion (load and split).
"""
import json
import tempfile
from pathlib import Path

import pytest
from langchain_core.documents import Document

from src.ingest import load_faq_json, load_all_raw_data, split_documents


def test_load_faq_json():
    data = [
        {"question": "Q1?", "answer": "A1", "category": "symptoms"},
        {"question": "Q2?", "answer": "A2"},
    ]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(data, f)
        path = Path(f.name)
    try:
        docs = load_faq_json(path)
        assert len(docs) == 2
        assert "Q1?" in docs[0].page_content
        assert "A1" in docs[0].page_content
        assert docs[0].metadata.get("category") == "symptoms"
    finally:
        path.unlink()


def test_split_documents():
    docs = [
        Document(page_content="First chunk. " * 100, metadata={"source": "a"}),
        Document(page_content="Second. " * 100, metadata={"source": "b"}),
    ]
    chunks = split_documents(docs)
    assert len(chunks) >= 2
    for c in chunks:
        assert isinstance(c, Document)
        assert len(c.page_content) > 0
