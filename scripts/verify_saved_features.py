
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

ROOT = Path(__file__).resolve().parent.parent

VIDEO = ROOT / "dataset/raw/learner_samples/learner_01/S02_father_learner_01_attempt01_20261020_085907.mp4"
FEATURES = ROOT / "dataset/processed/features/learner_01/S02_father_learner_01_attempt01_20261020_085907.npy"
MODEL = ROOT / "models/landmark_detectors/hand_landmarker.task"


def main():
    saved = np.load(FEATURES, allow_pickle=False)

    options = vision.HandLandmarkerOptions(
        base_options=python.BaseOptions(
            model_asset_path=str(MODEL)
        ),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=2,
    )

    capture = cv2.VideoCapture(str(VIDEO))
    if not capture.isOpened():
        raise RuntimeError(f"Cannot open video: {VIDEO}")

    fresh_rows = []
    timestamp_ms = -1

    try:
        with vision.HandLandmarker.create_from_options(options) as detector:
            while True:
                ok, frame = capture.read()
                if not ok:
                    break

                timestamp_ms += 34

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = mp.Image(
                    image_format=mp.ImageFormat.SRGB,
                    data=rgb,
                )
                result = detector.detect_for_video(image, timestamp_ms)

                left = np.zeros(63, dtype=np.float32)
                right = np.zeros(63, dtype=np.float32)

                hands = result.hand_landmarks or []
                labels = result.handedness or []

                for i, landmarks in enumerate(hands):
                    if i >= len(labels) or not labels[i]:
                        continue

                    label = labels[i][0].category_name.lower()
                    values = np.asarray(
                        [
                            coordinate
                            for point in landmarks
                            for coordinate in (point.x, point.y, point.z)
                        ],
                        dtype=np.float32,
                    )

                    if label == "left":
                        left = values
                    elif label == "right":
                        right = values

                fresh_rows.append(
                    np.concatenate([left, right])
                )
    finally:
        capture.release()

    fresh = np.asarray(fresh_rows, dtype=np.float32)

    print("Saved feature shape:", saved.shape)
    print("Fresh hand feature shape:", fresh.shape)

    if len(saved) != len(fresh):
        print("WARNING: Frame counts do not match.")
        return

    for name, start, end in (
        ("Left hand", 0, 63),
        ("Right hand", 63, 126),
    ):
        old = saved[:, start:end]
        new = fresh[:, start:end]

        old_valid = np.any(old != 0, axis=1)
        new_valid = np.any(new != 0, axis=1)
        common = old_valid & new_valid

        print(f"\n{name}")
        print("Saved frames with landmarks:", int(old_valid.sum()))
        print("Fresh frames with landmarks:", int(new_valid.sum()))
        print("Frames with landmarks in both:", int(common.sum()))

        if common.any():
            differences = np.abs(old[common] - new[common])
            print("Mean absolute difference:", float(differences.mean()))
            print("Maximum absolute difference:", float(differences.max()))
        else:
            print("No common detected frames to compare.")

    print("\nVerification complete. No files were modified.")


if __name__ == "__main__":
    main()
