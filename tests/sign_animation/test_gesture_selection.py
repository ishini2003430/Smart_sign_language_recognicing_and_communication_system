"""
tests/sign_animation/test_gesture_selection.py
===============================================
Tests for src/sign_animation/gesture_selection.py (SignDatabase)
"""

import json
import pytest
from pathlib import Path

from src.sign_animation.gesture_selection import SignDatabase, SignEntry


# ─── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture
def minimal_signs_json(tmp_path: Path) -> Path:
    """Write a minimal signs.json to a temp directory and return its path."""
    data = {
        "schema_version": "1.0",
        "signs": [
            {
                "sign_id": "T001",
                "label": "water",
                "sinhala_label": "වතුර",
                "video_path": "assets/sign_videos/T001_water.mp4",
                "expert": "test_expert",
                "language": "SLSL",
                "aliases": ["wattura"],
                "variants": [],
                "context_tags": ["basic_need"],
            },
            {
                "sign_id": "T002",
                "label": "mother",
                "sinhala_label": "අම්මා",
                "video_path": "assets/sign_videos/T002_mother.mp4",
                "expert": "test_expert",
                "language": "SLSL",
                "aliases": ["mom", "amma"],
                "variants": [],
                "context_tags": ["family"],
            },
        ],
    }
    signs_path = tmp_path / "signs.json"
    signs_path.write_text(json.dumps(data), encoding="utf-8")
    return signs_path


@pytest.fixture
def db(minimal_signs_json: Path) -> SignDatabase:
    return SignDatabase.load(path=minimal_signs_json, repo_root=minimal_signs_json.parent)


# ─── Loading ──────────────────────────────────────────────────────────────────


def test_load_valid_json(db: SignDatabase):
    assert len(db.all_signs()) == 2


def test_load_missing_file(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        SignDatabase.load(path=tmp_path / "nonexistent.json", repo_root=tmp_path)


def test_load_invalid_structure(tmp_path: Path):
    bad = tmp_path / "bad.json"
    bad.write_text('{"not_signs": []}', encoding="utf-8")
    with pytest.raises(ValueError):
        SignDatabase.load(path=bad, repo_root=tmp_path)


def test_load_missing_required_field(tmp_path: Path):
    data = {"signs": [{"sign_id": "X001"}]}  # missing label, video_path, expert
    path = tmp_path / "signs.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError):
        SignDatabase.load(path=path, repo_root=tmp_path)


# ─── Lookup — found ───────────────────────────────────────────────────────────


def test_lookup_primary_label(db: SignDatabase):
    entry = db.lookup("water")
    assert entry is not None
    assert entry.sign_id == "T001"


def test_lookup_case_insensitive(db: SignDatabase):
    assert db.lookup("Water") is not None
    assert db.lookup("WATER") is not None


def test_lookup_alias(db: SignDatabase):
    entry = db.lookup("mom")
    assert entry is not None
    assert entry.sign_id == "T002"


def test_lookup_sinhala_label(db: SignDatabase):
    entry = db.lookup("අම්මා")
    assert entry is not None
    assert entry.sign_id == "T002"


# ─── Lookup — not found ───────────────────────────────────────────────────────


def test_lookup_unknown_returns_none(db: SignDatabase):
    assert db.lookup("xyz_unknown_word") is None


def test_lookup_empty_string_returns_none(db: SignDatabase):
    assert db.lookup("") is None


# ─── Video existence ──────────────────────────────────────────────────────────


def test_video_not_found_reported(db: SignDatabase):
    # In the test fixture the video files don't exist on disk
    for entry in db.all_signs():
        assert entry.video_exists is False


def test_video_found_when_file_exists(tmp_path: Path):
    # Create the video file so video_exists becomes True
    video_file = tmp_path / "assets" / "sign_videos" / "T001_water.mp4"
    video_file.parent.mkdir(parents=True)
    video_file.write_bytes(b"fake_mp4_content")

    data = {
        "schema_version": "1.0",
        "signs": [
            {
                "sign_id": "T001",
                "label": "water",
                "video_path": "assets/sign_videos/T001_water.mp4",
                "expert": "test_expert",
                "language": "SLSL",
            }
        ],
    }
    signs_path = tmp_path / "signs.json"
    signs_path.write_text(json.dumps(data), encoding="utf-8")

    db = SignDatabase.load(path=signs_path, repo_root=tmp_path)
    entry = db.lookup("water")
    assert entry is not None
    assert entry.video_exists is True


# ─── Summary ──────────────────────────────────────────────────────────────────


def test_summary_structure(db: SignDatabase):
    s = db.summary()
    assert "total" in s
    assert "with_video" in s
    assert "signs" in s
    assert s["total"] == 2


# ─── Display label ────────────────────────────────────────────────────────────


def test_display_label_with_sinhala(db: SignDatabase):
    entry = db.lookup("water")
    assert entry is not None
    assert "water" in entry.display_label
    assert "වතුර" in entry.display_label


def test_display_label_without_sinhala():
    entry = SignEntry(
        sign_id="X001",
        label="test",
        video_path="some/path.mp4",
        expert="e1",
    )
    assert entry.display_label == "test"
