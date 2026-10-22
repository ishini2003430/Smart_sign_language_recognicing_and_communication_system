"""
animation_renderer.py
=====================
Replaceable interface for future 3D / avatar animation output.

Current status
--------------
A video-based renderer (video_renderer.py) is the production output for
the initial prototype.  This module defines the interface that a future
3D animation renderer must implement so it can be swapped in without
changing the rest of the pipeline.

No 3D avatar is fabricated here.  Calling render() on the stub below
raises NotImplementedError to make this explicit.

How to add a real 3D renderer
------------------------------
1. Create a subclass of AnimationRenderer.
2. Implement render() to return pose/keyframe data for the frontend avatar.
3. Pass the new renderer instance to AnimationService.
4. Adjust the frontend to consume the new output format.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class AnimationFrame:
    """
    A single frame of 3D avatar animation data.

    Fields are intentionally generic so different skeleton formats can be
    supported without changing the interface.
    """

    frame_index: int
    keypoints: dict[str, Any]
    """Arbitrary keypoint data (e.g. joint angles, XYZ positions)."""


@dataclass
class AnimationClip:
    """A sequence of frames for one sign."""

    sign_id: str
    label: str
    frames: list[AnimationFrame]
    fps: float = 30.0


class AnimationRenderer(ABC):
    """Abstract base class for animation renderers."""

    @abstractmethod
    def render(self, sign_id: str) -> Optional[AnimationClip]:
        """
        Return animation data for *sign_id*, or None if unavailable.

        Implementations must not fabricate data for signs they do not
        have validated assets for.
        """
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Return True if this renderer has assets loaded and is ready."""
        ...


class StubAnimationRenderer(AnimationRenderer):
    """
    Placeholder renderer used until a real 3D implementation is available.

    render() always raises NotImplementedError so callers know to fall back
    to video_renderer.py.
    """

    def render(self, sign_id: str) -> Optional[AnimationClip]:
        raise NotImplementedError(
            "3D animation is not yet implemented.  "
            "Use video_renderer.resolve_video_url() for the current prototype."
        )

    def is_available(self) -> bool:
        return False
