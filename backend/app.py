
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.sign_animation.animation_service import AnimationService


# --------------------------------------------------
# Project configuration
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent

# Directory where per-sign motion JSONs are stored (one file per sign_id).
# Created by backend/extract_all_motions.py.
MOTIONS_DIR = Path(__file__).resolve().parent / "motions"
MOTIONS_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title="SLSL Bidirectional Communication API",
    description="Text-to-Sri Lankan Sign Language video translation API",
    version="1.0.0",
)


# --------------------------------------------------
# CORS configuration
# Allows the React frontend to access the backend
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Serve sign language videos
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory=str(ROOT)),
    name="static",
)


# --------------------------------------------------
# Initialize the existing animation service
# --------------------------------------------------

service = AnimationService.create()


# --------------------------------------------------
# Request models
# --------------------------------------------------

class TranslationRequest(BaseModel):
    text: str


class RecognizedTextRequest(BaseModel):
    text: str
    recognized_by: str = "sign_recognition"


# --------------------------------------------------
# Health check endpoint
# --------------------------------------------------

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "message": "SLSL backend is running",
    }


# --------------------------------------------------
# Get all available signs
# --------------------------------------------------

@app.get("/api/signs")
def get_signs():
    signs = service.get_all_signs()
    return {"signs": signs}


# --------------------------------------------------
# Text-to-sign translation endpoint
# --------------------------------------------------

@app.post("/api/translation/text-to-sign")
def text_to_sign(request: TranslationRequest):

    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter some text.",
        )

    try:
        result = service.translate(request.text)

        matched_signs = []

        for item in result.playback_sequence:
            label = item.label
            word = label.split(" (")[0]

            matched_signs.append({
                "sign_id": item.sign_id,
                "word": word,
                "label": label,
                "video_found": item.available,
                "available": item.available,
                "video_url": item.video_url,
                "message": item.message,
            })

        return {
            "original_input": result.original_input,
            "matched_signs": matched_signs,
            "unsupported_words": result.missing_tokens,
            "coverage": result.coverage,
            "message": (
                f"Matched {len(matched_signs)} sign video(s)."
                if matched_signs
                else "No matching sign videos were found."
            ),
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Translation failed: {str(exc)}",
        ) from exc


# --------------------------------------------------
# Receive recognized text from the sign recognition module
# --------------------------------------------------

@app.post("/api/recognized-text")
def receive_recognized_text(request: RecognizedTextRequest):

    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Recognized text cannot be empty.",
        )

    try:
        result = service.accept_recognised_text(request.text)

        matched_signs = []
        for item in result.playback_sequence:
            label = item.label
            word = label.split(" (")[0]
            matched_signs.append({
                "sign_id": item.sign_id,
                "word": word,
                "label": label,
                "available": item.available,
                "video_url": item.video_url,
                "message": item.message,
            })

        return {
            "status": "success",
            "recognized_text": request.text,
            "recognized_by": request.recognized_by,
            "original_input": result.original_input,
            "matched_signs": matched_signs,
            "missing_tokens": result.missing_tokens,
            "coverage": result.coverage,
            "message": "Recognized text received and translated successfully.",
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Could not process recognized text: {str(exc)}",
        ) from exc


# --------------------------------------------------
# Serve per-sign motion JSON for the 3D avatar
# --------------------------------------------------

@app.get("/api/motion/{sign_id}")
def get_motion(sign_id: str):
    """
    Return the pre-extracted MediaPipe motion JSON for a given sign ID.

    The file must exist at backend/motions/<sign_id>.json.
    Run backend/extract_all_motions.py to generate these files.

    Returns 404 if the motion data is not yet available for this sign.
    """
    # Sanitise: sign IDs are alphanumeric + underscore only.
    safe_id = "".join(c for c in sign_id if c.isalnum() or c == "_")
    motion_file = MOTIONS_DIR / f"{safe_id}.json"

    if motion_file.exists():
        return FileResponse(
            path=str(motion_file),
            media_type="application/json",
            headers={
                "Cache-Control": "public, max-age=3600",
                "Access-Control-Allow-Origin": "*",
            },
        )

    # Not yet extracted — return a structured error so the frontend can
    # fall back gracefully (show video instead of avatar).
    raise HTTPException(
        status_code=404,
        detail=(
            f"Motion data for sign '{sign_id}' is not available yet. "
            "Run backend/extract_all_motions.py to generate it."
        ),
    )


@app.get("/api/motion")
def list_motions():
    """Return the list of sign IDs that have pre-extracted motion data."""
    available = [
        p.stem for p in sorted(MOTIONS_DIR.glob("*.json"))
    ]
    return {"available_sign_ids": available, "count": len(available)}
