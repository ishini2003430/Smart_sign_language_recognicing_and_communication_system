
from pathlib import Path
import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent

LEARNER = (
    ROOT / "dataset" / "raw" / "learner_samples" / "learner_01"
    / "S02_father_learner_01_attempt01_20261019_233302.mp4"
)

EXPERT = (
    ROOT / "dataset" / "raw" / "expert_reference" / "expert_02"
    / "S02_father.mp4"
)

OUTPUT = ROOT / "dataset" / "processed" / "video_inspection_frames" / (
    "S02_father_learner_vs_expert02.mp4"
)

PANEL_W = 640
PANEL_H = 480
HEADER_H = 45
OUTPUT_FPS = 15


def fit_frame(frame):
    h, w = frame.shape[:2]
    scale = min(PANEL_W / w, PANEL_H / h)
    nw, nh = int(w * scale), int(h * scale)

    resized = cv2.resize(frame, (nw, nh))
    canvas = np.zeros((PANEL_H, PANEL_W, 3), dtype=np.uint8)

    x = (PANEL_W - nw) // 2
    y = (PANEL_H - nh) // 2
    canvas[y:y + nh, x:x + nw] = resized
    return canvas


def read_video(path):
    cap = cv2.VideoCapture(str(path))

    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {path}")

    frames = []
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frames.append(frame)

    cap.release()

    if not frames:
        raise RuntimeError(f"No frames found: {path}")

    return frames


def main():
    if not LEARNER.exists():
        raise FileNotFoundError(f"Learner video missing: {LEARNER}")
    if not EXPERT.exists():
        raise FileNotFoundError(f"Expert video missing: {EXPERT}")

    learner_frames = read_video(LEARNER)
    expert_frames = read_video(EXPERT)

    total = max(len(learner_frames), len(expert_frames))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    size = (PANEL_W * 2, PANEL_H + HEADER_H)
    writer = cv2.VideoWriter(
        str(OUTPUT),
        cv2.VideoWriter_fourcc(*"mp4v"),
        OUTPUT_FPS,
        size
    )

    if not writer.isOpened():
        raise RuntimeError(f"Could not create output video: {OUTPUT}")

    try:
        for i in range(total):
            progress = i / max(total - 1, 1)

            li = round(progress * (len(learner_frames) - 1))
            ei = round(progress * (len(expert_frames) - 1))

            left = fit_frame(learner_frames[li])
            right = fit_frame(expert_frames[ei])

            header = np.zeros(
                (HEADER_H, PANEL_W * 2, 3), dtype=np.uint8
            )
            cv2.putText(
                header, "LEARNER - S02 FATHER",
                (15, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 2
            )
            cv2.putText(
                header, "EXPERT 02 - S02 FATHER",
                (PANEL_W + 15, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 2
            )

            panels = np.hstack((left, right))
            combined = np.vstack((header, panels))
            writer.write(combined)

    finally:
        writer.release()

    print("Comparison video created:")
    print(OUTPUT)
    print("Learner frames:", len(learner_frames))
    print("Expert frames:", len(expert_frames))
    print("Alignment: normalized video progress")
    print("Note: this does not automatically identify sign errors.")


if __name__ == "__main__":
    main()
