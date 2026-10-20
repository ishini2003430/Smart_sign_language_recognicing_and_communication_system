
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.routes.translation import router as translation_router


# Create the FastAPI application
app = FastAPI(
    title="SLSL Sign Animation API",
    description=(
        "Backend for the Smart Sri Lankan Sign Language "
        "Recognition and Communication System"
    ),
    version="1.0.0",
)


# Configure frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Original sign-language video dataset folder
DATASET_ROOT = Path(
    r"C:\Users\vihan\Documents\Smart_sign_language_recognicing_and_communication_system\expert_reference\expert_reference"
)


# Check that the dataset folder exists before starting the server
if not DATASET_ROOT.is_dir():
    raise RuntimeError(
        f"Sign-language dataset folder not found: {DATASET_ROOT}"
    )


# Make dataset videos accessible through the API
app.mount(
    "/api/videos",
    StaticFiles(directory=str(DATASET_ROOT)),
    name="sign-videos",
)


# Register the translation API
app.include_router(translation_router)


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "SLSL Sign Animation API is running"
    }


# Health-check endpoint
@app.get("/api/health")
def health():
    return {
        "status": "healthy"
    }
