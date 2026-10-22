"""
extract_all_motions.py
======================
Batch motion extractor.

Reads every sign from dataset/metadata/signs.json that has a video file
on disk and runs MediaPipe Holistic over it, saving one
backend/motions/<sign_id>.json per sign.

Usage (run from project root):
    python -m backend.extract_all_motions

Requirements:
    pip install mediapipe opencv-python

The output JSON format is the same frame-array format used by
AvatarViewer.jsx:
    [
        { "frame_index": 0, "time_seconds": 0.0,
          "pose": [...], "left_hand": [...], "right_hand": [...], "face": [] },
        ...
    ]
"""

import cv2
import json
import sys
from pathlib import Path

try:
    import mediapipe as mp
except ImportError:
    print("ERROR: mediapipe is not installed.  Run:  pip install mediapipe")
    sys.exit(1)


# ──────────────────────────────────────────────
# Paths
# ──────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SIGNS_JSON = PROJECT_ROOT / "dataset" / "metadata" / "signs.json"
MOTIONS_DIR = PROJECT_ROOT / "backend" / "motions"
MOTIONS_DIR.mkdir(parents=True, exist_ok=True)


# ──────────────────────────────────────────────
# Landmark helpers (same logic as extract_sign_motion.py)
# ──────────────────────────────────────────────

def _convert_landmarks(landmarks, include_visibility: bool = False) -> list:
    if landmarks is None:
        return []
    result = []
    for pt in landmarks.landmark:
        item = {"x": float(pt.x), "y": float(pt.y), "z": float(pt.z)}
        if include_visibility:
            item["visibility"] = float(getattr(pt, "visibility", 0.0))
        result.append(item)
    return result


# ──────────────────────────────────────────────
# Per-video extraction
# ──────────────────────────────────────────────

def extract_motion(video_path: Path, holistic) -> list:
    """Run holistic detection on *video_path* and return a list of frame dicts."""
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    frames = []
    frame_idx = 0

    while True:
        ok, image = cap.read()
        if not ok:
            break

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        results = holistic.process(rgb)

        frames.append({
            "frame_index": frame_idx,
            "time_seconds": round(frame_idx / fps, 5),
            "pose":       _convert_landmarks(results.pose_landmarks,      include_visibility=True),
            "left_hand":  _convert_landmarks(results.left_hand_landmarks),
            "right_hand": _convert_landmarks(results.right_hand_landmarks),
            "face":       _convert_landmarks(results.face_landmarks),
        })
        frame_idx += 1

    cap.release()
    return frames


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main() -> None:
    if not SIGNS_JSON.exists():
        print(f"ERROR: signs.json not found at {SIGNS_JSON}")
        sys.exit(1)

    with SIGNS_JSON.open("r", encoding="utf-8") as f:
        data = json.load(f)

    signs = data.get("signs", [])
    print(f"Found {len(signs)} signs in signs.json")
    print(f"Output directory: {MOTIONS_DIR}\n")

    mp_holistic = mp.solutions.holistic

    processed = 0
    skipped = 0
    errors = 0

    with mp_holistic.Holistic(
        static_image_mode=False,
        model_complexity=1,
        smooth_landmarks=True,
        refine_face_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as holistic:

        for sign in signs:
            sign_id: str   = sign.get("sign_id", "")
            label: str     = sign.get("label", sign_id)
            video_path_rel: str = sign.get("video_path", "")

            if not sign_id:
                print(f"  SKIP — no sign_id: {sign}")
                skipped += 1
                continue

            out_path = MOTIONS_DIR / f"{sign_id}.json"
            if out_path.exists():
                print(f"  [{sign_id}] {label:20s} → already extracted, skipping")
                skipped += 1
                continue

            # Resolve absolute video path
            abs_video = PROJECT_ROOT / video_path_rel
            if not abs_video.is_file():
                # Try searching expert_reference
                filename = Path(video_path_rel).name
                expert_root = PROJECT_ROOT / "expert_reference"
                matches = sorted(expert_root.rglob(filename)) if expert_root.is_dir() else []
                if matches:
                    abs_video = matches[0]
                else:
                    print(f"  [{sign_id}] {label:20s} → VIDEO NOT FOUND, skipping")
                    skipped += 1
                    continue

            print(f"  [{sign_id}] {label:20s} → extracting {abs_video.name} …", end=" ", flush=True)

            try:
                frames = extract_motion(abs_video, holistic)
                tmp = out_path.with_suffix(".tmp")
                with tmp.open("w", encoding="utf-8") as f:
                    json.dump(frames, f, ensure_ascii=False, separators=(",", ":"))
                tmp.replace(out_path)
                print(f"{len(frames)} frames → {out_path.name}")
                processed += 1
            except Exception as exc:
                print(f"ERROR: {exc}")
                errors += 1

    print(f"\n{'='*50}")
    print(f"Done.  Processed={processed}  Skipped={skipped}  Errors={errors}")
    print(f"Motion files saved to: {MOTIONS_DIR}")


if __name__ == "__main__":
    main()
