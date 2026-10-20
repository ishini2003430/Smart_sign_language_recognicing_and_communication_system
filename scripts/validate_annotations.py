
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
METADATA = ROOT / "dataset" / "annotations" / "learner_capture_metadata.csv"
LABELS = ROOT / "dataset" / "annotations" / "learner_labels.json"

VALID_ERROR_TAGS = {
    "hand_shape",
    "hand_position",
    "hand_movement",
}


def main():
    with METADATA.open("r", encoding="utf-8-sig", newline="") as f:
        recordings = list(csv.DictReader(f))

    with LABELS.open("r", encoding="utf-8") as f:
        annotations = json.load(f)

    if not isinstance(annotations, list):
        raise ValueError("Annotations must be a JSON list.")

    metadata_ids = [r["recording_id"] for r in recordings]
    annotation_ids = [a.get("recording_id") for a in annotations]

    errors = []

    if len(metadata_ids) != len(set(metadata_ids)):
        errors.append("Duplicate recording IDs in metadata.")

    if len(annotation_ids) != len(set(annotation_ids)):
        errors.append("Duplicate recording IDs in annotations.")

    missing = set(metadata_ids) - set(annotation_ids)
    extra = set(annotation_ids) - set(metadata_ids)

    if missing:
        errors.append(f"Missing annotations: {sorted(missing)}")
    if extra:
        errors.append(f"Unknown annotation IDs: {sorted(extra)}")

    for item in annotations:
        rid = item.get("recording_id", "<unknown>")

        for field in ("learner_id", "intended_form_id", "correct", "error_tags"):
            if field not in item:
                errors.append(f"{rid}: missing field '{field}'")

        correct = item.get("correct")
        if correct is not None and not isinstance(correct, bool):
            errors.append(f"{rid}: correct must be true, false, or null.")

        tags = item.get("error_tags")
        if not isinstance(tags, list):
            errors.append(f"{rid}: error_tags must be a list.")
        elif not set(tags).issubset(VALID_ERROR_TAGS):
            errors.append(f"{rid}: invalid error tags {tags}.")

        if correct is True and tags:
            errors.append(
                f"{rid}: marked correct but has error tags; review this label."
            )

    print(f"Metadata recordings: {len(recordings)}")
    print(f"Annotation records: {len(annotations)}")
    print(f"Pending review: {sum(a.get('correct') is None for a in annotations)}")

    if errors:
        print("\nVALIDATION FAILED:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("\nValidation passed: structure and recording IDs are consistent.")
    print("This does not verify whether the video labels are correct.")


if __name__ == "__main__":
    main()
