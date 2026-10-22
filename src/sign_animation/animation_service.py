"""
animation_service.py
====================
Orchestrator for the Text/Speech-to-Sign pipeline.

This module ties together all stages:
    text_processing → gloss_generation → gesture_selection → video_renderer

It is the single entry point used by the backend route (backend/routes/sign_animation.py).

The design is intentionally simple for the prototype.  Advanced features such
as contextual sign selection and 3D animation can be plugged in later by
extending this class or replacing individual stages.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from src.sign_animation.gesture_selection import SignDatabase
from src.sign_animation.gloss_generation import GlossSequence, GlossStatus, generate_gloss
from src.sign_animation.text_processing import NormalisedInput, normalise
from src.sign_animation.video_renderer import FallbackStrategy, VideoResult, resolve_sequence

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Response model
# ---------------------------------------------------------------------------


@dataclass
class TranslationResult:
    """
    Complete result of translating a text input into a sign sequence.

    Fields
    ------
    original_input:
        The raw text supplied by the user.
    normalised_text:
        Text after normalisation.
    language_hint:
        Detected language ('english', 'sinhala', 'unknown').
    tokens:
        Token list produced by text_processing.
    playback_sequence:
        Ordered list of VideoResult objects for the frontend player.
    missing_tokens:
        Tokens that had no matching sign in the database.
    coverage:
        Fraction of tokens that have a matching sign (0.0–1.0).
    warnings:
        Non-fatal notices from any pipeline stage.
    """

    original_input: str
    normalised_text: str
    language_hint: str
    tokens: list[str]
    playback_sequence: list[VideoResult]
    missing_tokens: list[str]
    coverage: float
    warnings: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------


class AnimationService:
    """
    Orchestrates the sign animation pipeline.

    Usage
    -----
    ::

        service = AnimationService.create()
        result = service.translate("I want water")
    """

    def __init__(
        self,
        db: SignDatabase,
        fallback_strategy: FallbackStrategy = FallbackStrategy.MESSAGE,
    ) -> None:
        self._db = db
        self._fallback = fallback_strategy

    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------

    @classmethod
    def create(
        cls,
        signs_json: Optional[Path] = None,
        repo_root: Optional[Path] = None,
        fallback_strategy: FallbackStrategy = FallbackStrategy.MESSAGE,
    ) -> "AnimationService":
        """
        Create an :class:`AnimationService` by loading the sign database.

        Parameters
        ----------
        signs_json:
            Path to signs.json.  Defaults to dataset/metadata/signs.json.
        repo_root:
            Repository root.  Defaults to two levels above this file.
        fallback_strategy:
            What to do when a requested sign video is missing on disk.
        """
        db = SignDatabase.load(path=signs_json, repo_root=repo_root)
        return cls(db=db, fallback_strategy=fallback_strategy)

    # ------------------------------------------------------------------
    # Pipeline
    # ------------------------------------------------------------------

    def translate(self, text: str) -> TranslationResult:
        """
        Run the full pipeline for a text input.

        Parameters
        ----------
        text:
            Raw user input (English or Sinhala).

        Returns
        -------
        TranslationResult
        """
        # Stage 1: Normalise
        norm: NormalisedInput = normalise(text)
        all_warnings: list[str] = list(norm.warnings)

        if not norm.tokens:
            return TranslationResult(
                original_input=text,
                normalised_text=norm.normalised,
                language_hint=norm.language_hint,
                tokens=[],
                playback_sequence=[],
                missing_tokens=[],
                coverage=0.0,
                warnings=all_warnings,
            )

        # Stage 2: Gloss generation
        gloss_seq: GlossSequence = generate_gloss(norm.tokens, self._db)

        if gloss_seq.missing:
            all_warnings.append(
                f"No sign found for: {', '.join(gloss_seq.missing)}.  "
                "These words will be skipped in the playback sequence.  "
                "The displayed text preserves the full input."
            )

        # Stage 3: Video resolution (only for tokens that matched)
        found_entries = [
            item.sign for item in gloss_seq.items if item.status == GlossStatus.FOUND
        ]
        playback = resolve_sequence(found_entries, self._fallback)  # type: ignore[arg-type]

        return TranslationResult(
            original_input=text,
            normalised_text=norm.normalised,
            language_hint=norm.language_hint,
            tokens=norm.tokens,
            playback_sequence=playback,
            missing_tokens=gloss_seq.missing,
            coverage=gloss_seq.coverage,
            warnings=all_warnings,
        )

    def get_all_signs(self) -> dict:
        """Return a summary of all available signs for the /api/signs endpoint."""
        return self._db.summary()

    def accept_recognised_text(self, text: str) -> TranslationResult:
        """
        Accept text produced by a teammate's sign-recognition module and feed
        it through the same pipeline as typed input.

        This method is the integration point for the recognition component.
        The caller (backend route) should distinguish recognised text from
        typed text in the response so the frontend can display them in
        separate sections.

        Parameters
        ----------
        text:
            The sentence or word produced by the recognition module.

        Returns
        -------
        TranslationResult
        """
        return self.translate(text)
