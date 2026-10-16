from pathlib import Path
import math

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# Project folder: the folder containing this Python file.
ROOT = Path(__file__).resolve().parents[1]

# Change this filename to "S08_friend.mp4" to preview friend.
VIDEO = (
    ROOT
    / "dataset"
    / "raw"
    / "expert_reference"
    / "expert_01"
    / "S12_home.mp4"
)

MODEL = ROOT / "models" / "mediapipe" / "hand_landmarker.task"

# 200 milliseconds gives a slower preview for inspection.
PREVIEW_DELAY_MS = 200

# Connections between the 21 landmarks on each hand.
CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),        # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),        # Index finger
    (5, 9), (9, 10), (10, 11), (11, 12),   # Middle finger
    (9, 13), (13, 14), (14, 15), (15, 16), # Ring finger
    (13, 17), (0, 17),                     # Palm
    (17, 18), (18, 19), (19, 20),           # Little finger
]


def main():
    if not VIDEO.is_file():
        raise FileNotFoundError(f"Video not found: {VIDEO}")

    if not MODEL.is_file():
        raise FileNotFoundError(f"Detector not found: {MODEL}")

    options = vision.HandLandmarkerOptions(
        base_options=python.BaseOptions(
            model_asset_path=str(MODEL)
        ),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=2,
    )

    cap = cv2.VideoCapture(str(VIDEO))

    if not cap.isOpened():
        cap.release()
        raise RuntimeError(f"Cannot open video: {VIDEO}")

    fps = cap.get(cv2.CAP_PROP_FPS)

    if not math.isfinite(fps) or fps <= 0:
        cap.release()
        raise RuntimeError("Cannot read a valid video frame rate.")

    frame_count = 0
    frames_with_hands = 0
    last_timestamp = -1
    window_name = "Hand landmarks - Q: quit | Space: pause"

    print(f"Video: {VIDEO.name}")
    print("Green dots = landmarks; white lines = connections.")
    print("Click the preview window to use the controls.")
    print("Press SPACE to pause, any key to resume, or Q to quit.")

    try:
        with vision.HandLandmarker.create_from_options(options) as detector:
            while True:
                ok, frame = cap.read()

                if not ok:
                    break

                timestamp_ms = max(
                    last_timestamp + 1,
                    round(frame_count * 1000 / fps),
                )
                last_timestamp = timestamp_ms

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                mp_image = mp.Image(
                    image_format=mp.ImageFormat.SRGB,
                    data=rgb,
                )

                result = detector.detect_for_video(
                    mp_image,
                    timestamp_ms,
                )

                height, width = frame.shape[:2]
                hands_found = len(result.hand_landmarks)

                if hands_found > 0:
                    frames_with_hands += 1

                for hand in result.hand_landmarks:
                    points = [
                        (
                            round(landmark.x * width),
                            round(landmark.y * height),
                        )
                        for landmark in hand
                    ]

                    # Draw lines before dots so dots remain visible.
                    for start, end in CONNECTIONS:
                        cv2.line(
                            frame,
                            points[start],
                            points[end],
                            (255, 255, 255),
                            2,
                            cv2.LINE_AA,
                        )

                    for point in points:
                        cv2.circle(
                            frame,
                            point,
                            4,
                            (0, 255, 0),
                            -1,
                        )

                cv2.putText(
                    frame,
                    f"Hands detected: {hands_found}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 255),
                    2,
                )

                cv2.putText(
                    frame,
                    f"File: {VIDEO.name}",
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 255),
                    1,
                )

                # Resize only the display, preserving its aspect ratio.
                preview_height = 650
                preview_width = round(width * preview_height / height)

                preview = cv2.resize(
                    frame,
                    (preview_width, preview_height),
                )

                cv2.imshow(window_name, preview)
                frame_count += 1

                key = cv2.waitKey(PREVIEW_DELAY_MS) & 0xFF

                if key == ord(" "):
                    key = cv2.waitKey(0) & 0xFF

                if key in (ord("q"), ord("Q"), 27):
                    break

                if cv2.getWindowProperty(
                    window_name, cv2.WND_PROP_VISIBLE
                ) < 1:
                    break

    finally:
        cap.release()
        cv2.destroyAllWindows()

    print(f"Frames processed: {frame_count}")
    print(
        "Frames with at least one detected hand: "
        f"{frames_with_hands}"
    )

    if frame_count > 0:
        coverage = 100 * frames_with_hands / frame_count
        print(f"Hand detection coverage: {coverage:.1f}%")

    print("This preview does not predict sign meanings or save landmarks.")


if __name__ == "__main__":
    main()