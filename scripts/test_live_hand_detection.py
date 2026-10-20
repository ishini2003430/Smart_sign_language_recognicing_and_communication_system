
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parent.parent
MODEL = ROOT / "models" / "landmark_detectors" / "hand_landmarker.task"

options = vision.HandLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path=str(MODEL)),
    running_mode=vision.RunningMode.VIDEO,
    num_hands=2,
)

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Could not open webcam.")
    raise SystemExit(1)

start = time.monotonic()
last_timestamp = -1
frame_count = 0
frames_with_hands = 0
max_hands = 0
label_counts = {"Left": 0, "Right": 0, "Unknown": 0}

print("Test running for 10 seconds. Keep your hands visible.")

try:
    with vision.HandLandmarker.create_from_options(options) as detector:
        while time.monotonic() - start < 10:
            ok, frame = camera.read()
            if not ok:
                print("ERROR: Could not read camera frame.")
                break

            timestamp = int((time.monotonic() - start) * 1000)
            timestamp = max(timestamp, last_timestamp + 1)
            last_timestamp = timestamp

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb,
            )
            result = detector.detect_for_video(image, timestamp)

            hands = result.hand_landmarks or []
            labels = result.handedness or []

            frame_count += 1
            max_hands = max(max_hands, len(hands))

            if hands:
                frames_with_hands += 1

            names = []
            for i in range(len(hands)):
                label = "Unknown"
                if i < len(labels) and labels[i]:
                    label = labels[i][0].category_name

                names.append(label)
                label_counts[label if label in label_counts else "Unknown"] += 1

            if frame_count % 15 == 0:
                print(
                    f"Frame {frame_count}: "
                    f"{len(hands)} hand(s), labels={names}"
                )

            cv2.imshow("Hand test - Q to quit", frame)
            if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q"), 27):
                break

finally:
    camera.release()
    cv2.destroyAllWindows()

print("\n=== DETECTION SUMMARY ===")
print(f"Frames processed: {frame_count}")
print(f"Frames with at least one hand: {frames_with_hands}")
print(f"Maximum hands detected in one frame: {max_hands}")
print(f"Hand label counts: {label_counts}")
print("Webcam released.")
