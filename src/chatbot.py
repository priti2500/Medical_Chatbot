"""
Chatbot orchestration: validation, RAG query, disclaimers, and conversation logging.
"""
import logging
from typing import List, Tuple

from src.utils import validate_query, sanitize_for_display
from src.rag import build_rag_chain, query_rag

logger = logging.getLogger(__name__)

# Footer appended to every bot reply for safety
DISCLAIMER_FOOTER = (
    "\n\n— This is for general information only, not medical advice. "
    "Please consult a healthcare provider for your situation."
)


def get_chatbot_chain():
    """Build and return the RAG chain (lazy load vector store)."""
    return build_rag_chain()


def chat(
    user_message: str,
    rag_chain,
    conversation_history: List[Tuple[str, str]] | None = None,
) -> Tuple[str, str | None]:
    """
    Process one user message and return (bot_reply, error_message).
    If error_message is not None, bot_reply may be empty or a fallback message.
    """
    is_valid, err = validate_query(user_message)
    if not is_valid:
        return "", err

    conversation_history = conversation_history or []
    try:
        result = query_rag(user_message, rag_chain, chat_history=conversation_history)
        answer = result.get("answer", "").strip()
        if not answer:
            answer = (
                "I couldn't find enough relevant information to answer that. "
                "Please rephrase or consult a healthcare provider."
            )
        # Keep responses user-friendly and append disclaimer
        answer = sanitize_for_display(answer)
        answer = answer + DISCLAIMER_FOOTER
        return answer, None
    except FileNotFoundError as e:
        logger.exception("Vector store not found: %s", e)
        return "", (
            "The knowledge base is not ready. Please run: python scripts/build_vector_store.py"
        )
    except ValueError as e:
        logger.warning("Configuration error: %s", e)
        return "", str(e)
    except Exception as e:
        logger.exception("RAG query failed: %s", e)
        return "", (
            "Something went wrong while answering. Please try again or rephrase your question."
        )


def get_disclaimer() -> str:
    """Return the full disclaimer text for UI display."""
    from config.settings import DISCLAIMER
    return DISCLAIMER
