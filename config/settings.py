"""
Application settings loaded from environment variables.
Centralizes config for LLM, vector store, and safety limits.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# -----------------------------------------------------------------------------
# API Keys (Groq LLM)
# -----------------------------------------------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# -----------------------------------------------------------------------------
# Vector Store (FAISS - local, no external API key)
# -----------------------------------------------------------------------------
VECTOR_STORE_PATH = Path(os.getenv("VECTOR_STORE_PATH", "vector_store/faiss_index"))

# Pinecone (optional)
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_ENV = os.getenv("PINECONE_ENV", "us-east-1")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "medical-chatbot")

# Weaviate (optional)
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY", "")

# -----------------------------------------------------------------------------
# RAG & LLM (Groq + HuggingFace embeddings)
# -----------------------------------------------------------------------------
# Number of document chunks to retrieve for context
MAX_CONTEXT_DOCS = int(os.getenv("MAX_CONTEXT_DOCS", "4"))
# Groq model name (can be overridden in .env)
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
# Max tokens for chatbot response (keep responses short)
MAX_RESPONSE_TOKENS = int(os.getenv("MAX_RESPONSE_TOKENS", "350"))

# -----------------------------------------------------------------------------
# Chat & Safety
# -----------------------------------------------------------------------------
# Max messages to keep in session history (for context window)
CHAT_HISTORY_LIMIT = int(os.getenv("CHAT_HISTORY_LIMIT", "20"))
# Disclaimer text shown to users
DISCLAIMER = (
    "This chatbot provides general health information only and does not replace "
    "professional medical advice, diagnosis, or treatment. Always seek the advice of "
    "your physician or other qualified health provider with any questions."
)

# -----------------------------------------------------------------------------
# Data paths
# -----------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
