"""
gloss_generation.py
===================
Stage 2 of the Text/Speech-to-Sign pipeline.

Responsibilities
----------------
- Accept the token list produced by text_processing.normalise().
- Attempt to map each token to a sign identifier (gloss ID) using the
  loaded sign registry.
- Return an ordered gloss sequence with explicit FOUND / NOT_FOUND status
  for each token.

What this module does NOT do
-----------------------------
- It does NOT perform linguistic sign-order rewriting (SOV → SLSL order).
  That requires expert-validated grammar rules which are out of scope for
  the initial prototype.
- It does NOT silently substitute an unrelated sign for an unknown token.
- It does NOT translate Sinhala words into English before matching; callers
  must pass tokens that the registry can match.

Design principle
----------------
Every mapping must be traceable to the signs.json registry.  If a token
has no confirmed mapping, the result is marked NOT_FOUND and the caller
decides what to do (show a message, skip, finger-spell, etc.).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from src.sign_animation.gesture_selection import SignDatabase, SignEntry


class GlossStatus(str, Enum):
    FOUND = "found"
    NOT_FOUND = "not_found"


@dataclass
class GlossItem:
    """A single token with its resolution status."""

    token: str
    """The normalised input token."""

    status: GlossStatus
    """Whether a matching sign was found in the registry."""

    sign: SignEntry | None = None
    """The matched sign entry, or None when status is NOT_FOUND."""


@dataclass
class GlossSequence:
    """The result of mapping a full token list to a sign sequence."""

    items: list[GlossItem] = field(default_factory=list)

    @property
    def found(self) -> list[GlossItem]:
        return [i for i in self.items if i.status == GlossStatus.FOUND]

    @property
    def missing(self) -> list[str]:
        return [i.token for i in self.items if i.status == GlossStatus.NOT_FOUND]

    @property
    def coverage(self) -> float:
        """Fraction of tokens that have a matching sign (0.0–1.0)."""
        if not self.items:
            return 0.0
        return len(self.found) / len(self.items)


def generate_gloss(tokens: list[str], db: SignDatabase) -> GlossSequence:
    """
    Map *tokens* to gloss items using *db*.

    Parameters
    ----------
    tokens:
        Ordered normalised tokens from text_processing.normalise().
    db:
        A loaded :class:`~gesture_selection.SignDatabase` instance.

    Returns
    -------
    GlossSequence
        An ordered sequence of GlossItems, one per input token.
    """
    items: list[GlossItem] = []

    for token in tokens:
        entry = db.lookup(token)
        if entry is not None:
            items.append(
                GlossItem(token=token, status=GlossStatus.FOUND, sign=entry)
            )
        else:
            items.append(
                GlossItem(token=token, status=GlossStatus.NOT_FOUND, sign=None)
            )

    return GlossSequence(items=items)
