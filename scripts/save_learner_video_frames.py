
from pathlib import Path
import cv2

ROOT = Path(__file__).resolve().parent.parent

VIDEOS = {
    "learner_attempt01": (
        ROOT / "dataset" / "raw" / "learner_samples" / "learner_01"
        / "S02_father_learner_01_attempt01_20261019_233302.mp4"
    ),
    "expert_02": (
        ROOT / "dataset" / "raw" / "expert_reference" / "expert_02"
        / "S02_father.mp4"
    ),
}

OUTPUT = ROOT / "dataset" / "processed" / "video_inspection_frames"
OUTPUT.mkdir(parents=True, exist_ok=True)

for video_name, video_path in VIDEOS.items():
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        print(f"ERROR: Could not open video: {video_path}")
        continue

    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total <= 0:
        print(f"ERROR: No frames found in {video_path}")
        cap.release()
        continue

    positions = sorted(set([
        0,
        total // 4,
        total // 2,
        (3 * total) // 4,
        total - 1,
    ]))

    for frame_number in positions:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ok, frame = cap.read()

        if ok:
            output_path = OUTPUT / (
                f"{video_name}_frame_{frame_number:04d}.jpg"
            )
            if cv2.imwrite(str(output_path), frame):
                print("Saved:", output_path)
            else:
                print("ERROR: Could not save:", output_path)

    print(f"{video_name}: {total} total frames processed.")
    cap.release()

print("Frame extraction finished. Original videos were not modified.")
