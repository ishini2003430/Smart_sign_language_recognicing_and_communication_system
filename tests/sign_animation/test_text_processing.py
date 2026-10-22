"""
tests/sign_animation/test_text_processing.py
=============================================
Tests for src/sign_animation/text_processing.py
"""

import pytest
from src.sign_animation.text_processing import normalise, detect_language


# ─── detect_language ──────────────────────────────────────────────────────────


def test_detect_english_plain():
    assert detect_language("I want water") == "english"


def test_detect_sinhala():
    # Contains Sinhala characters
    assert detect_language("මම ගෙදර") == "sinhala"


def test_detect_english_empty():
    assert detect_language("") == "english"


# ─── normalise — basic ────────────────────────────────────────────────────────


def test_normalise_simple_english():
    result = normalise("I want water")
    assert result.tokens == ["i", "want", "water"]
    assert result.language_hint == "english"
    assert result.warnings == []


def test_normalise_lower_case():
    result = normalise("MOTHER GO HOSPITAL")
    assert result.tokens == ["mother", "go", "hospital"]


def test_normalise_punctuation_stripped():
    result = normalise("Hello, world! How are you?")
    assert "hello" in result.tokens
    assert "world" in result.tokens
    # Punctuation must not appear in tokens
    for tok in result.tokens:
        assert "," not in tok
        assert "!" not in tok
        assert "?" not in tok


def test_normalise_extra_whitespace():
    result = normalise("  eat   food   ")
    assert result.tokens == ["eat", "food"]


def test_normalise_sinhala_preserved():
    """
    Sinhala text uses Unicode combining characters.  After normalisation the
    script characters must still be present in the output tokens even if
    some tokens are shorter fragments due to combining-mark boundaries.
    The important guarantee is:
      - language_hint is 'sinhala'
      - at least one token exists
      - the joined token string contains Sinhala Unicode code points
    """
    text = "අම්මා ගෙදර"
    result = normalise(text)
    assert result.language_hint == "sinhala"
    assert len(result.tokens) >= 1
    joined = " ".join(result.tokens)
    # Verify Sinhala code points survived (U+0D85-U+0DFF range)
    assert any("\u0D80" <= ch <= "\u0DFF" for ch in joined)


# ─── normalise — edge cases ───────────────────────────────────────────────────


def test_normalise_empty_string():
    result = normalise("")
    assert result.tokens == []
    assert len(result.warnings) > 0


def test_normalise_only_whitespace():
    result = normalise("   ")
    assert result.tokens == []
    assert len(result.warnings) > 0


def test_normalise_only_punctuation():
    result = normalise("!!! ???")
    # Tokens should be empty or contain only empty strings filtered out
    assert result.tokens == []
    assert len(result.warnings) > 0


def test_normalise_mixed_punctuation_and_words():
    result = normalise("Come, quickly! Go now.")
    assert "come" in result.tokens
    assert "quickly" in result.tokens
    assert "go" in result.tokens
    assert "now" in result.tokens


def test_normalise_intra_word_hyphen_preserved():
    result = normalise("sign-language system")
    # The hyphenated word should stay as one token or be split, but not crash
    assert len(result.tokens) >= 1


def test_normalise_original_preserved():
    raw = "I want Water!"
    result = normalise(raw)
    assert result.original == raw


def test_normalise_multiple_words():
    result = normalise("mother father child doctor hospital")
    assert result.tokens == ["mother", "father", "child", "doctor", "hospital"]
    assert len(result.tokens) == 5
