"""
Unit tests for input validation and sanitization.
"""
import pytest
from src.utils import validate_query, sanitize_for_display


def test_validate_query_empty():
    valid, err = validate_query("")
    assert not valid
    assert "enter" in err.lower() or "query" in err.lower()


def test_validate_query_whitespace_only():
    valid, err = validate_query("   \n\t  ")
    assert not valid


def test_validate_query_none():
    valid, err = validate_query(None)
    assert not valid


def test_validate_query_valid():
    valid, err = validate_query("What are symptoms of flu?")
    assert valid
    assert err == ""


def test_validate_query_too_long():
    valid, err = validate_query("x" * 3000)
    assert not valid
    assert "long" in err.lower()


def test_sanitize_for_display_none():
    assert sanitize_for_display(None) == ""


def test_sanitize_for_display_truncate():
    long_text = "a" * 10000
    out = sanitize_for_display(long_text, max_len=100)
    assert len(out) <= 100
    assert out.endswith("...")
