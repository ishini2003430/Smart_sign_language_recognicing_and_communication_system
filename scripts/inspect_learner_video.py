
from pathlib import Path
import cv2

ROOT = Path(__file__).resolve().parent.parent

VIDEO = ROOT / "dataset" / "raw" / "learner_samples" / "learner_01" / (
    "S02_father_learner_01_attempt02_20261019_233333.mp4"
)

cap = cv2.VideoCapture(str(VIDEO))

if not cap.isOpened():
    raise RuntimeError(f"Could not open video: {VIDEO}")

print("Controls:")
print("  SPACE = pause/resume")
print("  RIGHT ARROW = next frame while paused")
print("  Q or ESC = quit")

paused = False

try:
    while True:
        if not paused:
            ok, frame = cap.read()
            if not ok:
                print("Reached end of video.")
                break

        cv2.imshow("Inspect learner video - S02 Father", frame)
        key = cv2.waitKey(0 if paused else 30) & 0xFF

        if key in (ord("q"), 27):
            break
        elif key == ord(" "):
            paused = not paused
        elif key == 83 and paused:  # Right arrow on many Windows setups
            ok, frame = cap.read()
            if not ok:
                break

finally:
    cap.release()
    cv2.destroyAllWindows()
