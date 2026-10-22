"""
tests/sign_animation/test_animation_service.py
===============================================
Integration tests for the full text-to-sign pipeline via AnimationService.
"""

import json
import pytest
from pathlib import Path

from src.sign_animation.animation_service import AnimationService


# ─── Fixture ──────────────────────────────────────────────────────────────────


@pytest.fixture
def service(tmp_path: Path) -> AnimationService:
    """Return an AnimationService with a small in-memory sign database."""
    data = {
        "schema_version": "1.0",
        "signs": [
            {
                "sign_id": "T001",
                "label": "water",
                "sinhala_label": "වතුර",
                "video_path": "assets/sign_videos/T001_water.mp4",
                "expert": "test",
                "language": "SLSL",
                "aliases": ["wattura"],
            },
            {
                "sign_id": "T002",
                "label": "mother",
                "sinhala_label": "අම්මා",
                "video_path": "assets/sign_videos/T002_mother.mp4",
                "expert": "test",
                "language": "SLSL",
                "aliases": ["mom"],
            },
            {
                "sign_id": "T003",
                "label": "go",
                "sinhala_label": "යන්න",
                "video_path": "assets/sign_videos/T003_go.mp4",
                "expert": "test",
                "language": "SLSL",
                "aliases": [],
            },
        ],
    }
    signs_path = tmp_path / "signs.json"
    signs_path.write_text(json.dumps(data), encoding="utf-8")
    return AnimationService.create(signs_json=signs_path, repo_root=tmp_path)


# ─── Pipeline — known words ───────────────────────────────────────────────────


def test_translate_single_known_word(service: AnimationService):
    result = service.translate("water")
    assert result.coverage == 1.0
    assert len(result.playback_sequence) == 1
    assert result.playback_sequence[0].sign_id == "T001"
    assert result.missing_tokens == []


def test_translate_multiple_known_words(service: AnimationService):
    result = service.translate("mother go")
    assert len(result.playback_sequence) == 2
    assert result.missing_tokens == []


def test_translate_preserves_order(service: AnimationService):
    result = service.translate("mother go water")
    ids = [vr.sign_id for vr in result.playback_sequence]
    assert ids == ["T002", "T003", "T001"]


# ─── Pipeline — unknown words ─────────────────────────────────────────────────


def test_translate_unknown_word_reported(service: AnimationService):
    result = service.translate("hello world")
    assert "hello" in result.missing_tokens
    assert "world" in result.missing_tokens
    assert result.coverage == 0.0
    assert len(result.warnings) > 0


def test_translate_mixed_known_unknown(service: AnimationService):
    result = service.translate("mother hello")
    assert len(result.playback_sequence) == 1
    assert "hello" in result.missing_tokens
    assert 0 < result.coverage < 1.0


# ─── Pipeline — empty input ───────────────────────────────────────────────────


def test_translate_empty_string(service: AnimationService):
    result = service.translate("")
    assert result.playback_sequence == []
    assert len(result.warnings) > 0


def test_translate_only_whitespace(service: AnimationService):
    result = service.translate("   ")
    assert result.playback_sequence == []


# ─── Pipeline — alias lookup ──────────────────────────────────────────────────


def test_translate_via_alias(service: AnimationService):
    result = service.translate("mom")
    assert len(result.playback_sequence) == 1
    assert result.playback_sequence[0].sign_id == "T002"


# ─── Video URL ────────────────────────────────────────────────────────────────


def test_video_url_absent_when_file_missing(service: AnimationService):
    result = service.translate("water")
    vr = result.playback_sequence[0]
    # Video file was not created in the fixture, so it should be unavailable
    assert vr.available is False
    assert vr.video_url is None
    assert vr.message is not None


def test_video_url_present_when_file_exists(tmp_path: Path):
    # Create the actual video file
    video_file = tmp_path / "assets" / "sign_videos" / "T001_water.mp4"
    video_file.parent.mkdir(parents=True)
    video_file.write_bytes(b"fake_mp4")

    data = {
        "schema_version": "1.0",
        "signs": [
            {
                "sign_id": "T001",
                "label": "water",
                "video_path": "assets/sign_videos/T001_water.mp4",
                "expert": "test",
                "language": "SLSL",
            }
        ],
    }
    signs_path = tmp_path / "signs.json"
    signs_path.write_text(json.dumps(data), encoding="utf-8")
    svc = AnimationService.create(signs_json=signs_path, repo_root=tmp_path)

    result = svc.translate("water")
    vr = result.playback_sequence[0]
    assert vr.available is True
    assert vr.video_url is not None
    assert "T001_water.mp4" in vr.video_url


# ─── Recognised text integration ─────────────────────────────────────────────


def test_accept_recognised_text_same_as_translate(service: AnimationService):
    t = service.translate("mother go water")
    r = service.accept_recognised_text("mother go water")
    assert t.tokens == r.tokens
    assert t.coverage == r.coverage
