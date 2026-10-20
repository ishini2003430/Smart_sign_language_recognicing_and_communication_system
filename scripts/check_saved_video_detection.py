
from pathlib import Path
from collections import Counter

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

ROOT = Path(__file__).resolve().parent.parent

VIDEO = ROOT / "dataset" / "raw" / "learner_samples" / "learner_01" / (
    "S02_father_learner_01_attempt01_20261020_085907.mp4"
)

FEATURES = ROOT / "dataset" / "processed" / "features" / "learner_01" / (
    "S02_father_learner_01_attempt01_20261020_085907.npy"
)

MODEL = ROOT / "models" / "landmark_detectors" / "hand_landmarker.task"


def main():
    for path in (VIDEO, FEATURES, MODEL):
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

    saved = np.load(FEATURES, allow_pickle=False)

    print("=== Existing feature file ===")
    print("Shape:", saved.shape)

    for name, start, end in (
        ("Left", 0, 63),
        ("Right", 63, 126),
    ):
        block = saved[:, start:end].reshape(len(saved), 21, 3)
        detected_frames = np.any(block != 0, axis=(1, 2)).sum()
        print(
            f"{name} hand: nonzero landmarks in "
            f"{detected_frames}/{len(saved)} frames"
        )

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
    timestamp_ms = -1

    print("\n=== Re-detecting hands in saved video ===")

    try:
        with vision.HandLandmarker.create_from_options(options) as detector:
            while True:
                ok, frame = camera.read()
                if not ok:
                    break

                timestamp_ms += 34
                total_frames += 1

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
                    print(
                        f"Frame {total_frames}: "
                        f"{len(hands)} hand(s)"
                    )

    finally:
        camera.release()

    print("\n=== Video detection summary ===")
    print("Frames processed:", total_frames)
    print("Frames with at least one hand:", frames_with_hands)
    print("Detected-hand label counts:", dict(counts))
    print("Video and feature frame counts match:", total_frames == len(saved))


if __name__ == "__main__":
    main()
