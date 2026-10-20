from pathlib import Path

DATASET_ROOT = Path(
    r"C:\Users\vihan\Documents\Smart_sign_language_recognicing_and_communication_system\expert_reference\expert_reference"
)

VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}

if not DATASET_ROOT.exists():
    print(f"Dataset folder not found: {DATASET_ROOT}")
else:
    videos = sorted(
        p for p in DATASET_ROOT.rglob("*")
        if p.is_file() and p.suffix.lower() in VIDEO_EXTENSIONS
    )

    print(f"Dataset location: {DATASET_ROOT}")
    print(f"Total videos found: {len(videos)}")