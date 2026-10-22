"""
video_renderer.py
=================
Stage 4 of the Text/Speech-to-Sign pipeline (output side).

Responsibilities
----------------
- Accept a SignEntry and return a URL that the frontend can use to play
  the sign video via a standard HTML <video> element.
- Validate that the video file is accessible before returning a URL.
- Provide a configurable fallback strategy when a video is missing.

What this module does NOT do
-----------------------------
- It does NOT render or generate 3D animation (see animation_renderer.py
  for the replaceable interface).
- It does NOT stream or transcode video; it relies on the FastAPI static-
  file server to serve the files.
- It does NOT fabricate video URLs for signs that have no confirmed recording.

Fallback strategy
-----------------
The FallbackStrategy enum controls what happens when a requested video is
absent:

  NONE    – Return None; the caller must handle the gap.
  MESSAGE – Return a structured error dict; the UI shows a "not available"
            notice.

The strategy is selected in animation_service.py and can be changed
without touching this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from src.sign_animation.gesture_selection import SignEntry


class FallbackStrategy(str, Enum):
    NONE = "none"
    MESSAGE = "message"


@dataclass
class VideoResult:
    """Result returned by :func:`resolve_video_url`."""

    sign_id: str
    label: str
    video_url: Optional[str]
    """
    Relative URL served by FastAPI, e.g.
    '/static/sign_videos/S001_mother.mp4'.
    None when the video is missing and strategy is NONE.
    """

    available: bool
    """True if the video file exists and the URL is valid."""

    message: Optional[str] = None
    """Human-readable message when a sign is unavailable."""


# Prefix served by the FastAPI static mount (see backend/app.py).
_STATIC_PREFIX = "/static"


def resolve_video_url(
    entry: SignEntry,
    strategy: FallbackStrategy = FallbackStrategy.MESSAGE,
) -> VideoResult:
    """
    Convert a :class:`~gesture_selection.SignEntry` into a
    :class:`VideoResult` that carries a playable URL.

    Parameters
    ----------
    entry:
        The sign to render.
    strategy:
        What to do when the video file is missing on disk.

    Returns
    -------
    VideoResult
    """
    if entry.video_exists:
        # Build the URL served by the FastAPI static file mount.
        # video_path is relative to repo root, e.g.
        # "assets/sign_videos/S001_mother.mp4"
        url = f"{_STATIC_PREFIX}/{entry.video_path}"
        return VideoResult(
            sign_id=entry.sign_id,
            label=entry.display_label,
            video_url=url,
            available=True,
        )

    # Video is missing —————————————————————————————————————————————————
    msg = (
        f"Video not available for '{entry.display_label}' ({entry.sign_id}). "
        "The sign is registered but the video file has not been added yet. "
        "Please contact the project administrator to add the recording."
    )

    if strategy == FallbackStrategy.NONE:
        return VideoResult(
            sign_id=entry.sign_id,
            label=entry.display_label,
            video_url=None,
            available=False,
            message=msg,
        )

    # Default: MESSAGE strategy
    return VideoResult(
        sign_id=entry.sign_id,
        label=entry.display_label,
        video_url=None,
        available=False,
        message=msg,
    )


def resolve_sequence(
    entries: list[SignEntry],
    strategy: FallbackStrategy = FallbackStrategy.MESSAGE,
) -> list[VideoResult]:
    """
    Resolve a list of sign entries to video results in order.

    Parameters
    ----------
    entries:
        Ordered list of :class:`SignEntry` objects from the gloss sequence.
    strategy:
        Fallback behaviour for missing videos.

    Returns
    -------
    list[VideoResult]
        Same order as *entries*.
    """
    return [resolve_video_url(e, strategy) for e in entries]
