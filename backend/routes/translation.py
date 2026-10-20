
import re
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/translation",
    tags=["Translation"],
)

# Original dataset folder. Videos stay in this location.
DATASET_ROOT = Path(
    r"C:\Users\vihan\Documents\Smart_sign_language_recognicing_and_communication_system\expert_reference\expert_reference"
)

VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}

# English words mapped to dataset filename labels.
AVAILABLE_SIGNS = {
    "amma": "amma",
    "father": "father",
    "daughter": "daughter",
    "go": "go",
    "come": "come",
    "welcome": "welcome",
    "school": "school",
    "friend": "friend",
    "sister": "sister",
    "son": "son",
    "brother": "brother",
    "home": "home",
    "eat": "eat",
    "i": "I",
    "you": "You",
    "want": "want",
    "water": "water",
    "see": "see",
    "month": "month",
    "friday": "friday",
    "february": "february",
    "me": "me",
    "mine": "mine",
    "how": "how",
    "drink": "drink",
    "why": "why",
    "think": "think",
    "know": "know",
    "look": "look",
    "colombo": "colombo",
}

# Match filenames exactly, ignoring letter case.
def find_video(label: str):
    if not DATASET_ROOT.exists():
        return None

    target = label.casefold()

    for path in DATASET_ROOT.rglob("*"):
        if (
            path.is_file()
            and path.suffix.lower() in VIDEO_EXTENSIONS
            and path.stem.split("_", 1)[-1].casefold() == target
        ):
            # Return a URL path served by the backend, not a Windows path.
            relative_path = path.relative_to(DATASET_ROOT).as_posix()
            return f"/api/videos/{relative_path}"

    return None


class TranslationRequest(BaseModel):
    text: str = Field(min_length=1, max_length=1000)


@router.post("/text-to-sign")
def text_to_sign(request: TranslationRequest):
    words = re.findall(r"[a-z]+", request.text.lower())

    matched_signs = []
    unsupported_words = []

    for word in words:
        label = AVAILABLE_SIGNS.get(word)

        if label is None:
            unsupported_words.append(word)
            continue

        video_url = find_video(label)

        matched_signs.append({
            "word": word,
            "label": label,
            "video_url": video_url,
            "video_found": video_url is not None,
        })

    return {
        "input_text": request.text,
        "matched_signs": matched_signs,
        "unsupported_words": unsupported_words,
        "message": (
            "Sign labels processed successfully."
            if matched_signs
            else "No supported signs found."
        ),
    }
