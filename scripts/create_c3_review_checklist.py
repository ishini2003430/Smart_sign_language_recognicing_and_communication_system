
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LABELS = ROOT / "dataset" / "annotations" / "learner_labels.json"

# Use a new filename to avoid the existing file permission error.
OUTPUT = (
    ROOT
    / "dataset"
    / "annotations"
    / "c3_review_checklist_v2.csv"
)


def main():
    # Check that the annotation file exists.
    if not LABELS.exists():
        print(f"ERROR: Annotation file not found:\n{LABELS}")
        return

    # Load existing learner annotation records.
    try:
        with LABELS.open("r", encoding="utf-8") as f:
            records = json.load(f)
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON in learner_labels.json:\n{exc}")
        return
    except OSError as exc:
        print(f"ERROR: Cannot read annotation file:\n{exc}")
        return

    if not isinstance(records, list):
        print("ERROR: Expected learner_labels.json to contain a JSON list.")
        return

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    columns = [
        "recording_id",
        "learner_id",
        "intended_form_id",
        "overall_correct",
        "hand_shape_error",
        "hand_position_error",
        "hand_movement_error",
        "reviewer_id",
        "review_notes",
    ]

    rows = []

    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            print(f"WARNING: Skipping invalid record at index {index}.")
            continue

        # Preserve the existing recording identifiers.
        rows.append({
            "recording_id": record.get("recording_id", ""),
            "learner_id": record.get("learner_id", ""),
            "intended_form_id": record.get("intended_form_id", ""),
            "overall_correct": "pending",
            "hand_shape_error": "pending",
            "hand_position_error": "pending",
            "hand_movement_error": "pending",
            "reviewer_id": "",
            "review_notes": "Needs video review",
        })

    try:
        with OUTPUT.open(
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)

    except PermissionError:
        print("ERROR: Windows denied permission to create the checklist.")
        print("Close Excel or another program using the output file.")
        print(f"Output path: {OUTPUT}")
        return
    except OSError as exc:
        print(f"ERROR: Could not create the checklist:\n{exc}")
        return

    print("=" * 55)
    print("C3 LEARNER REVIEW CHECKLIST CREATED")
    print("=" * 55)
    print(f"Output file: {OUTPUT}")
    print(f"Recordings included: {len(rows)}")
    print("All labels remain pending until reviewed.")
    print("The original learner_labels.json was not modified.")
    print("=" * 55)


if __name__ == "__main__":
    main()
