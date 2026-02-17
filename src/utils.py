"""
Utility functions: input validation, error handling, and safe text processing.
"""
import re
import logging
from typing import Optional

# Configure module logger
logger = logging.getLogger(__name__)

# Max length for user query (prevent abuse and token overflow)
MAX_QUERY_LENGTH = 2000

# Patterns to detect potentially harmful or non-medical content (basic filter)
BLOCKED_PATTERNS = [
    r"\b( prescribe | dosage | mg | mcg | units )\s*\d+",  # dosage requests
]


def validate_query(query: Optional[str]) -> tuple[bool, str]:
    """
    Validate user input for safety and length.
    Returns (is_valid, error_message).
    """
    if query is None:
        return False, "No query provided."
    if not isinstance(query, str):
        return False, "Invalid input type."
    stripped = query.strip()
    if not stripped:
        return False, "Please enter a question."
    if len(stripped) > MAX_QUERY_LENGTH:
        return False, f"Query is too long. Please keep it under {MAX_QUERY_LENGTH} characters."
    # Block obvious dosage-style requests (informational only – we don't prescribe)
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, stripped, re.IGNORECASE):
            logger.warning(f"Blocked query matching pattern: {pattern}")
            return False, (
                "I can't provide specific dosing. Please ask your doctor or pharmacist "
                "for dosage information."
            )
    return True, ""


def sanitize_for_display(text: Optional[str], max_len: int = 5000) -> str:
    """Ensure text is safe for display and truncate if needed."""
    if text is None:
        return ""
    s = str(text).strip()
    if len(s) > max_len:
        s = s[: max_len - 3] + "..."
    return s


def setup_logging(level: int = logging.INFO) -> None:
    """Configure root logger for the application."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
