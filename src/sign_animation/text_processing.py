"""
text_processing.py
==================
Stage 1 of the Text/Speech-to-Sign pipeline.

Responsibilities
----------------
- Accept raw English or Sinhala text from a user or speech recogniser.
- Normalise the input (lower-case, strip punctuation, collapse whitespace).
- Split the result into a flat list of tokens (words / short phrases).
- Return a structured result that carries both the original and normalised
  forms so nothing is silently discarded.

What this module does NOT do
-----------------------------
- It does NOT look up signs.
- It does NOT translate Sinhala text into English.
- It does NOT claim any word maps to a sign; that is handled by
  gesture_selection.py.

Language note
-------------
SLSL is a natural language.  Simple word-for-word tokenisation is a first
approximation only.  Linguistic rules and expert-validated gloss mappings
will be added in a later iteration.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class NormalisedInput:
    """Holds the result of text normalisation for a single user utterance."""

    original: str
    """The raw string exactly as received."""

    normalised: str
    """Lower-cased, punctuation-stripped, whitespace-collapsed text."""

    tokens: list[str]
    """Ordered list of non-empty tokens after normalisation."""

    language_hint: str
    """'english', 'sinhala', or 'unknown'."""

    warnings: list[str] = field(default_factory=list)
    """Non-fatal notices for the caller (e.g. empty input)."""


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

# Sinhala Unicode block: U+0D80–U+0DFF
_SINHALA_RE = re.compile(r"[\u0D80-\u0DFF]")


def detect_language(text: str) -> str:
    """Return 'sinhala' if the text contains Sinhala characters, else 'english'."""
    if _SINHALA_RE.search(text):
        return "sinhala"
    return "english"


def normalise(raw: str) -> NormalisedInput:
    """
    Normalise *raw* text and return a :class:`NormalisedInput`.

    Steps
    -----
    1. Strip leading/trailing whitespace.
    2. Detect language.
    3. Unicode NFC normalisation.
    4. Remove punctuation characters (ASCII and common Unicode).
    5. Collapse multiple spaces into one.
    6. Lower-case (safe for Sinhala since it has no case).
    7. Split into tokens.

    Parameters
    ----------
    raw:
        The user-supplied string. May be English, Sinhala, or mixed.

    Returns
    -------
    NormalisedInput
        A structured object with the original, normalised text, token list,
        language hint, and any warnings.
    """
    warnings: list[str] = []

    # Guard: empty input
    if not raw or not raw.strip():
        return NormalisedInput(
            original=raw,
            normalised="",
            tokens=[],
            language_hint="unknown",
            warnings=["Input is empty or contains only whitespace."],
        )

    original = raw
    lang = detect_language(raw)

    # NFC normalisation ensures consistent Unicode representation.
    text = unicodedata.normalize("NFC", raw)

    # Remove punctuation.  We keep hyphens inside words (e.g. "sign-language")
    # and apostrophes inside words but strip standalone ones.
    text = _strip_punctuation(text)

    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Lower-case (ASCII only for English; harmless for Sinhala)
    text = text.lower()

    tokens = [t for t in text.split(" ") if t]

    if not tokens:
        warnings.append(
            "No tokens remain after normalisation.  "
            "The input may consist entirely of punctuation."
        )

    return NormalisedInput(
        original=original,
        normalised=text,
        tokens=tokens,
        language_hint=lang,
        warnings=warnings,
    )


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _strip_punctuation(text: str) -> str:
    """
    Remove punctuation characters while preserving intra-word hyphens and
    Sinhala characters (which have category 'Lo').
    """
    result: list[str] = []
    for i, ch in enumerate(text):
        cat = unicodedata.category(ch)
        # Keep letters, digits, and whitespace.
        if cat.startswith("L") or cat.startswith("N") or cat.startswith("Z"):
            result.append(ch)
        # Keep intra-word hyphens (surrounded by word characters).
        elif ch == "-":
            prev_ok = i > 0 and (
                unicodedata.category(text[i - 1]).startswith("L")
                or unicodedata.category(text[i - 1]).startswith("N")
            )
            next_ok = i < len(text) - 1 and (
                unicodedata.category(text[i + 1]).startswith("L")
                or unicodedata.category(text[i + 1]).startswith("N")
            )
            if prev_ok and next_ok:
                result.append(ch)
            else:
                result.append(" ")
        else:
            # Replace other punctuation with space so token boundaries are
            # preserved.
            result.append(" ")
    return "".join(result)
