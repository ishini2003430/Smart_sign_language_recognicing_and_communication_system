
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
metadata_path = ROOT / "dataset" / "annotations" / "learner_capture_metadata.csv"
labels_path = ROOT / "dataset" / "annotations" / "learner_labels.json"

with metadata_path.open("r", encoding="utf-8-sig", newline="") as f:
    metadata = list(csv.DictReader(f))

with labels_path.open("r", encoding="utf-8-sig") as f:
    labels = json.load(f)

existing_ids = {item["recording_id"] for item in labels}
added = []

for row in metadata:
    recording_id = row["recording_id"]

    if recording_id in existing_ids:
        continue

    feature_path = ROOT / row["feature_path"]
    if not feature_path.is_file():
        print(f"Skipping missing feature file: {recording_id}")
        continue

    labels.append({
        "recording_id": recording_id,
        "learner_id": row["learner_id"],
        "intended_form_id": row["intended_form_id"],
        "correct": None,
        "error_tags": [],
        "staged_error": False,
        "valid_variant": None,
        "reviewer_id": None,
        "notes": "Needs video review"
    })
    added.append(recording_id)

with labels_path.open("w", encoding="utf-8") as f:
    json.dump(labels, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"Existing annotation records preserved: {len(existing_ids)}")
print(f"New records added: {len(added)}")

for recording_id in added:
    print("ADDED:", recording_id)

print(f"Total annotation records now: {len(labels)}")
