"""
speech_processing.py
====================
Optional speech-to-text stage for the Text/Speech-to-Sign pipeline.

Implementation note
-------------------
Browser-based speech recognition is handled entirely on the frontend using
the Web Speech API (webkitSpeechRecognition / SpeechRecognition).  This
module exists to:

1. Document the speech processing stage clearly.
2. Provide a server-side fallback using Python's SpeechRecognition library
   if a future version of the system needs server-side transcription
   (e.g. for devices without Web Speech API support).
3. Define a clean interface so the backend route can call it without
   depending on implementation details.

Current status
--------------
The Web Speech API approach is supported natively in Chromium-based browsers
(Chrome, Edge) and is available for free with no API key.  Firefox and Safari
have partial or no support.  The frontend shows a graceful error if the API is
unavailable.

The server-side fallback requires the 'SpeechRecognition' Python package and
a working microphone accessible to the server process, which is uncommon in
a web-server deployment.  It is therefore marked EXPERIMENTAL and disabled by
default.

To enable it, install:
    pip install SpeechRecognition

No paid APIs or cloud accounts are used.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class SpeechResult:
    """Holds the outcome of a speech recognition attempt."""

    transcript: Optional[str]
    """The recognised text, or None if recognition failed."""

    confidence: Optional[float]
    """Confidence score (0.0–1.0) if available; None otherwise."""

    error: Optional[str]
    """Human-readable error message if recognition failed."""

    source: str = "frontend_web_speech_api"
    """Which recogniser produced this result."""


# ---------------------------------------------------------------------------
# Frontend-first approach
# ---------------------------------------------------------------------------


def frontend_speech_note() -> str:
    """
    Return a message for the API health or info endpoint explaining that
    speech-to-text is handled by the browser Web Speech API, not this server.
    """
    return (
        "Speech recognition is handled by the browser's Web Speech API.  "
        "No audio is sent to this server.  The recognised text is forwarded "
        "to the /api/translate endpoint directly from the frontend.  "
        "This approach works in Chrome and Edge; Firefox/Safari may not support it."
    )


# ---------------------------------------------------------------------------
# Server-side fallback (EXPERIMENTAL — disabled by default)
# ---------------------------------------------------------------------------


def transcribe_audio_bytes(
    audio_bytes: bytes,
    language: str = "en-US",
) -> SpeechResult:
    """
    Attempt server-side transcription using the SpeechRecognition library.

    This function is NOT used in the standard pipeline.  It is provided for
    research experiments or devices that cannot use the Web Speech API.

    Parameters
    ----------
    audio_bytes:
        Raw WAV audio data.
    language:
        BCP-47 language code, e.g. 'en-US' or 'si-LK'.

    Returns
    -------
    SpeechResult
    """
    try:
        import io
        import speech_recognition as sr  # type: ignore[import]
    except ImportError:
        return SpeechResult(
            transcript=None,
            confidence=None,
            error=(
                "The 'SpeechRecognition' Python package is not installed.  "
                "Install it with: pip install SpeechRecognition"
            ),
            source="server_fallback",
        )

    recogniser = sr.Recognizer()
    try:
        audio_file = io.BytesIO(audio_bytes)
        with sr.AudioFile(audio_file) as source:
            audio = recogniser.record(source)
        # Google Web Speech API (free tier, no key required)
        text = recogniser.recognize_google(audio, language=language)
        return SpeechResult(
            transcript=text,
            confidence=None,  # Google free tier does not return confidence
            error=None,
            source="server_fallback_google_free",
        )
    except sr.UnknownValueError:
        return SpeechResult(
            transcript=None,
            confidence=None,
            error="Speech not understood.  Please speak clearly and try again.",
            source="server_fallback",
        )
    except sr.RequestError as exc:
        return SpeechResult(
            transcript=None,
            confidence=None,
            error=f"Speech recognition service error: {exc}",
            source="server_fallback",
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unexpected error in speech transcription")
        return SpeechResult(
            transcript=None,
            confidence=None,
            error=f"Unexpected error: {exc}",
            source="server_fallback",
        )
