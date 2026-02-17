"""
Test the RAG pipeline with example queries (no UI).
Run after building the vector store and setting GROQ_API_KEY in .env.

Usage:
    python scripts/test_queries.py
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils import setup_logging
from src.chatbot import get_chatbot_chain, chat

# Example test queries (short, user-friendly scope)
EXAMPLE_QUERIES = [
    "What are common flu symptoms?",
    "How much water should I drink per day?",
    "Can I take ibuprofen with aspirin?",
    "When should I see a doctor for a headache?",
    "What are signs of dehydration?",
]


def main():
    setup_logging()
    print("Loading RAG chain...")
    try:
        chain = get_chatbot_chain()
    except Exception as e:
        print(f"Failed to load chain: {e}")
        return 1
    print("Running example queries:\n")
    for q in EXAMPLE_QUERIES:
        print(f"Q: {q}")
        reply, err = chat(q, chain, conversation_history=[])
        if err:
            print(f"A: [Error] {err}\n")
        else:
            print(f"A: {reply[:400]}...\n" if len(reply) > 400 else f"A: {reply}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
