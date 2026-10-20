
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
METADATA = ROOT / "dataset" / "annotations" / "learner_capture_metadata.csv"
LABELS = ROOT / "dataset" / "annotations" / "learner_labels.json"

def main():
    with METADATA.open("r", encoding="utf-8-sig", newline="") as f:
        recordings = list(csv.DictReader(f))

    if not LABELS.exists():
        raise FileNotFoundError(f"Annotation file not found: {LABELS}")

    with LABELS.open("r", encoding="utf-8") as f:
        annotations = json.load(f)

    if not isinstance(annotations, list):
        raise ValueError("Expected learner_labels.json to contain a JSON list.")

    existing_ids = {item["recording_id"] for item in annotations}
    added = 0

    for recording in recordings:
        recording_id = recording["recording_id"]

        if recording_id in existing_ids:
            continue

        annotation = {
            "recording_id": recording_id,
            "learner_id": recording["learner_id"],
            "intended_form_id": recording["intended_form_id"],
            "correct": None,
            "error_tags": [],
            "staged_error": False,
            "valid_variant": None,
            "reviewer_id": None,
            "notes": "Needs video review"
        }

        annotations.append(annotation)
        existing_ids.add(recording_id)
        added += 1

    if len(existing_ids) != len(annotations):
        raise ValueError("Duplicate recording IDs detected; file not saved.")

    with LABELS.open("w", encoding="utf-8") as f:
        json.dump(annotations, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Metadata recordings: {len(recordings)}")
    print(f"Annotation records: {len(annotations)}")
    print(f"New records added: {added}")
    print("All new records remain pending video review.")

if __name__ == "__main__":
    main()
