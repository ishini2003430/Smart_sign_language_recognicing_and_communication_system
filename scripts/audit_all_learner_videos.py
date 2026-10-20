
from pathlib import Path
import csv

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

ROOT = Path(__file__).resolve().parent.parent
VIDEO_DIR = ROOT / "dataset" / "raw" / "learner_samples" / "learner_01"
FEATURE_DIR = ROOT / "dataset" / "processed" / "features" / "learner_01"
MODEL = ROOT / "models" / "landmark_detectors" / "hand_landmarker.task"
OUTPUT = ROOT / "dataset" / "processed" / "learner_video_detection_audit.csv"


def main():
    if not MODEL.exists():
        raise FileNotFoundError(f"Hand model not found: {MODEL}")

    videos = sorted(VIDEO_DIR.glob("*.mp4"))
    if not videos:
        print("No learner videos found:", VIDEO_DIR)
        return

    rows = []

    for video_path in videos:
        feature_path = FEATURE_DIR / f"{video_path.stem}.npy"
        camera = cv2.VideoCapture(str(video_path))

        if not camera.isOpened():
            print("COULD NOT OPEN:", video_path.name)
            camera.release()
            continue

        total = 0
        frames_with_hands = 0
        left_frames = 0
        right_frames = 0
        unknown_frames = 0

        options = vision.HandLandmarkerOptions(
            base_options=python.BaseOptions(
                model_asset_path=str(MODEL)
            ),
            running_mode=vision.RunningMode.VIDEO,
            num_hands=2,
        )

        try:
            # A fresh detector gives each video its own timestamp timeline.
            with vision.HandLandmarker.create_from_options(options) as detector:
                while True:
                    ok, frame = camera.read()
                    if not ok:
                        break

                    total += 1
                    timestamp_ms = round((total - 1) * 1000 / 30)

                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image = mp.Image(
                        image_format=mp.ImageFormat.SRGB,
                        data=rgb,
                    )

                    result = detector.detect_for_video(image, timestamp_ms)
                    hands = result.hand_landmarks or []
                    labels = result.handedness or []

                    if hands:
                        frames_with_hands += 1

                    frame_labels = set()
                    for i in range(len(hands)):
                        label = "Unknown"
                        if i < len(labels) and labels[i]:
                            label = labels[i][0].category_name
                        frame_labels.add(label)

                    if "Left" in frame_labels:
                        left_frames += 1
                    if "Right" in frame_labels:
                        right_frames += 1
                    if "Unknown" in frame_labels:
                        unknown_frames += 1
        finally:
            camera.release()

        saved_frames = ""
        frame_match = "feature file missing"

        if feature_path.exists():
            saved = np.load(feature_path, allow_pickle=False)
            if saved.ndim == 2:
                saved_frames = len(saved)
                frame_match = str(saved_frames == total)
            else:
                frame_match = f"invalid feature shape {saved.shape}"

        detection_pct = round(100 * frames_with_hands / total, 2) if total else 0

        row = {
            "video": video_path.name,
            "video_frames": total,
            "frames_with_any_hand": frames_with_hands,
            "any_hand_detection_pct": detection_pct,
            "frames_with_left_label": left_frames,
            "frames_with_right_label": right_frames,
            "frames_with_unknown_label": unknown_frames,
            "feature_frames": saved_frames,
            "frame_count_match": frame_match,
        }
        rows.append(row)

        print(f"\nVideo: {video_path.name}")
        print(f"Frames: {total}")
        print(f"Any hand detected: {frames_with_hands}/{total} ({detection_pct}%)")
        print(f"Left label in frames: {left_frames}")
        print(f"Right label in frames: {right_frames}")
        print(f"Unknown label in frames: {unknown_frames}")
        print(f"Feature/video frame match: {frame_match}")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    if rows:
        with OUTPUT.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    print("\nAudit saved to:", OUTPUT)
    print("No video or feature files were modified.")


if __name__ == "__main__":
    main()
