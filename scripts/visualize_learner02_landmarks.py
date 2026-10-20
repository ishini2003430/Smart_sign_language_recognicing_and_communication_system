
from pathlib import Path

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
    if not VIDEO.exists():
        raise FileNotFoundError(f"Video not found: {VIDEO}")
    if not MODEL.exists():
        raise FileNotFoundError(f"Model not found: {MODEL}")

    options = vision.HandLandmarkerOptions(
        base_options=python.BaseOptions(model_asset_path=str(MODEL)),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=2,
    )

    cap = cv2.VideoCapture(str(VIDEO))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {VIDEO}")

    connections = vision.HandLandmarksConnections.HAND_CONNECTIONS
    frame_number = 0

    try:
        with vision.HandLandmarker.create_from_options(options) as detector:
            while True:
                ok, frame = cap.read()
                if not ok:
                    break

                timestamp_ms = round(frame_number * 1000 / 30)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = mp.Image(
                    image_format=mp.ImageFormat.SRGB,
                    data=rgb,
                )

                result = detector.detect_for_video(image, timestamp_ms)
                hands = result.hand_landmarks or []

                for hand in hands:
                    points = [
                        (int(lm.x * frame.shape[1]),
                         int(lm.y * frame.shape[0]))
                        for lm in hand
                    ]

                    for connection in connections:
                        start = connection.start
                        end = connection.end
                        cv2.line(
                            frame, points[start], points[end],
                            (0, 255, 0), 2
                        )

                    for x, y in points:
                        cv2.circle(frame, (x, y), 4, (0, 0, 255), -1)

                cv2.putText(
                    frame,
                    f"Frame: {frame_number + 1} | Hands: {len(hands)}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (255, 255, 0),
                    2,
                )

                cv2.imshow("Learner 02 - Hand Landmarks", frame)

                key = cv2.waitKey(33) & 0xFF
                if key in (ord("q"), 27):
                    break

                frame_number += 1

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
