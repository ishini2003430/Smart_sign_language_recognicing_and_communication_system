"""
tests/sign_animation/test_api.py
=================================
API-level tests for the sign animation FastAPI endpoints.
Uses HTTPX's AsyncClient via TestClient for synchronous tests.
"""

import json
import pytest
from pathlib import Path
from fastapi.testclient import TestClient


# ─── App setup ────────────────────────────────────────────────────────────────


@pytest.fixture
def client(tmp_path: Path, monkeypatch):
    """
    Create a TestClient with a minimal sign database injected.
    The backend.routes.sign_animation module uses a module-level _service;
    we initialise it with a temp database before creating the client.
    """
    # Write a minimal signs.json
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
                "aliases": [],
            },
        ],
    }
    signs_path = tmp_path / "signs.json"
    signs_path.write_text(json.dumps(data), encoding="utf-8")

    # Patch the config so the app uses our temp file
    import backend.config as cfg
    monkeypatch.setattr(cfg, "SIGNS_JSON", signs_path)
    monkeypatch.setattr(cfg, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(cfg, "STATIC_DIR", tmp_path)

    from backend.app import app
    from backend.routes.sign_animation import init_service

    # Reinitialise service with our temp db
    init_service(signs_json=signs_path)

    with TestClient(app, raise_server_exceptions=True) as c:
        yield c


# ─── /api/health ──────────────────────────────────────────────────────────────


def test_health_returns_200(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200


def test_health_body_fields(client):
    body = client.get("/api/health").json()
    assert "status" in body
    assert "database_loaded" in body
    assert "signs_registered" in body
    assert body["database_loaded"] is True


# ─── /api/signs ───────────────────────────────────────────────────────────────


def test_signs_returns_200(client):
    resp = client.get("/api/signs")
    assert resp.status_code == 200


def test_signs_body_structure(client):
    body = client.get("/api/signs").json()
    assert "total" in body
    assert "signs" in body
    assert body["total"] == 1


def test_signs_entry_fields(client):
    entry = client.get("/api/signs").json()["signs"][0]
    for field in ("sign_id", "label", "video_path", "video_exists"):
        assert field in entry


# ─── /api/translate ───────────────────────────────────────────────────────────


def test_translate_known_word(client):
    resp = client.post("/api/translate", json={"text": "water"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["coverage"] == 1.0
    assert len(body["playback_sequence"]) == 1
    assert body["playback_sequence"][0]["sign_id"] == "T001"


def test_translate_unknown_word(client):
    resp = client.post("/api/translate", json={"text": "hello"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["coverage"] == 0.0
    assert "hello" in body["missing_tokens"]
    assert len(body["warnings"]) > 0


def test_translate_empty_text_rejected(client):
    resp = client.post("/api/translate", json={"text": ""})
    assert resp.status_code == 422


def test_translate_whitespace_only_rejected(client):
    resp = client.post("/api/translate", json={"text": "   "})
    assert resp.status_code == 422


def test_translate_preserves_original_input(client):
    resp = client.post("/api/translate", json={"text": "Water!"})
    body = resp.json()
    assert body["original_input"] == "Water!"


def test_translate_response_fields(client):
    body = client.post("/api/translate", json={"text": "water"}).json()
    for field in (
        "original_input",
        "normalised_text",
        "language_hint",
        "tokens",
        "coverage",
        "missing_tokens",
        "warnings",
        "playback_sequence",
    ):
        assert field in body


# ─── /api/recognized-text ────────────────────────────────────────────────────


def test_recognized_text_known_word(client):
    resp = client.post(
        "/api/recognized-text",
        json={"text": "water", "recognized_by": "test_recogniser"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["recognized_by"] == "test_recogniser"
    assert len(body["playback_sequence"]) == 1


def test_recognized_text_empty_rejected(client):
    resp = client.post(
        "/api/recognized-text",
        json={"text": "", "recognized_by": "test"},
    )
    assert resp.status_code == 422
