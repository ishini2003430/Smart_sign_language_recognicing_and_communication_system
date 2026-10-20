
import csv
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "dataset" / "annotations" / "learner_capture_metadata.csv"
LABELS = ROOT / "dataset" / "annotations" / "learner_labels.json"

ERROR_TAGS = {
    "1": "hand_shape",
    "2": "hand_position",
    "3": "hand_movement",
}


def open_video(path):
    if not path.is_file():
        print(f"Video not found: {path}")
        return

    # Opens the video using the default Windows video player.
    os.startfile(str(path))


with METADATA.open("r", encoding="utf-8-sig", newline="") as f:
    recordings = list(csv.DictReader(f))

with LABELS.open("r", encoding="utf-8") as f:
    labels = json.load(f)

labels_by_id = {item["recording_id"]: item for item in labels}

for recording in recordings:
    recording_id = recording["recording_id"]
    label = labels_by_id.get(recording_id)

    if label is None:
        print(f"Skipping: no annotation record for {recording_id}")
        continue

    if label.get("correct") is not None:
        continue

    learner_video = ROOT / recording["video_path"]

    print("\n" + "=" * 65)
    print(f"Recording: {recording_id}")
    print(f"Sign: {recording['intended_form_id']}")
    print(f"Learner: {recording['learner_id']}")
    print(f"Video: {learner_video}")
    print("Review this video against the matching expert reference.")
    print("1 = Correct sign")
    print("2 = Incorrect sign")
    print("S = Open learner video")
    print("Q = Save and quit")

    while True:
        choice = input("Your choice: ").strip().lower()

        if choice == "s":
            open_video(learner_video)
        elif choice == "q":
            with LABELS.open("w", encoding="utf-8") as f:
                json.dump(labels, f, indent=2, ensure_ascii=False)
                f.write("\n")
            print("Annotations saved. You can continue reviewing later.")
            raise SystemExit
        elif choice == "1":
            label["correct"] = True
            label["error_tags"] = []
            break
        elif choice == "2":
            label["correct"] = False
            print("Select every observed error category.")
            print("Enter 1, 2, 3 separated by commas.")
            print("1 = Hand shape; 2 = Hand position; 3 = Hand movement")
            print("Example: 1,3")
            selected = input("Error categories: ").strip()
            chosen = {
                item.strip()
                for item in selected.split(",")
                if item.strip()
            }

            if not chosen or not chosen.issubset(ERROR_TAGS):
                print("Invalid selection. Please enter 1, 2, or 3.")
                label["correct"] = None
                continue

            label["error_tags"] = [
                ERROR_TAGS[key] for key in sorted(chosen)
            ]
            break
        else:
            print("Enter 1, 2, S, or Q.")

    label["reviewer_id"] = "reviewer_01"
    label["notes"] = "Reviewed against expert reference"
    label["staged_error"] = False
    label["valid_variant"] = None

    with LABELS.open("w", encoding="utf-8") as f:
        json.dump(labels, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print("Annotation saved.")
    
print("\nReview session complete.")
print("Run the readiness checker to see the remaining pending labels.")
