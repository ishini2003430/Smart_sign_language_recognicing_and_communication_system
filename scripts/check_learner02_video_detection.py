
from pathlib import Path
from collections import Counter

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

ROOT = Path(__file__).resolve().parent.parent

VIDEO = (
    ROOT / "dataset" / "raw" / "learner_samples" / "learner_02"
    / "S02_father_learner_02_attempt01_20261020_093314.mp4"
)

MODEL = ROOT / "models" / "landmark_detectors" / "hand_landmarker.task"


def main():
    for path in (VIDEO, MODEL):
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

    options = vision.HandLandmarkerOptions(
        base_options=python.BaseOptions(
            model_asset_path=str(MODEL)
        ),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=2,
    )

    camera = cv2.VideoCapture(str(VIDEO))
    if not camera.isOpened():
        raise RuntimeError(f"Could not open video: {VIDEO}")

    counts = Counter()
    frames_with_hands = 0
    total_frames = 0

    try:
        with vision.HandLandmarker.create_from_options(options) as detector:
            while True:
                ok, frame = camera.read()
                if not ok:
                    break

                total_frames += 1
                timestamp_ms = round(
                    (total_frames - 1) * 1000 / 30
                )

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

                for i in range(len(hands)):
                    label = "Unknown"
                    if i < len(labels) and labels[i]:
                        label = labels[i][0].category_name
                    counts[label] += 1

                if total_frames % 15 == 0:
                    print(f"Frame {total_frames}: {len(hands)} hand(s)")

    finally:
        camera.release()

    print("\n=== Learner 02 detection summary ===")
    print("Frames processed:", total_frames)
    print("Frames with at least one detected hand:", frames_with_hands)
    print(
        "Hand detection rate:",
        f"{100 * frames_with_hands / total_frames:.2f}%"
        if total_frames else "N/A",
    )
    print("Detected-hand label counts:", dict(counts))


if __name__ == "__main__":
    main()
