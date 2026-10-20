
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent

LABELS_FILE = ROOT / "dataset" / "annotations" / "learner_labels.json"
FEATURES_DIR = ROOT / "dataset" / "processed" / "features"

with LABELS_FILE.open("r", encoding="utf-8") as f:
    records = json.load(f)

print("=" * 60)
print("C3 SUPERVISED TRAINING DATA READINESS CHECK")
print("=" * 60)

ready = 0
pending = 0
missing_features = 0
invalid_features = 0
seen_ids = set()

for record in records:
    recording_id = record.get("recording_id")
    learner_id = record.get("learner_id", "")
    label = record.get("correct")
    tags = record.get("error_tags", [])

    if recording_id in seen_ids:
        print(f"DUPLICATE RECORDING ID: {recording_id}")
    seen_ids.add(recording_id)

    feature_path = FEATURES_DIR / learner_id / f"{recording_id}.npy"

    if not feature_path.exists():
        print(f"MISSING FEATURE: {recording_id}")
        missing_features += 1
        continue

    try:
        features = np.load(feature_path, allow_pickle=False)
    except Exception as exc:
        print(f"UNREADABLE FEATURE: {recording_id}: {exc}")
        invalid_features += 1
        continue

    if features.ndim != 2 or features.shape[1] != 225:
        print(
            f"UNEXPECTED FEATURE SHAPE: {recording_id}: "
            f"{features.shape} (expected frames x 225)"
        )
        invalid_features += 1
        continue

    if not np.isfinite(features).all():
        print(f"NON-FINITE VALUES: {recording_id}")
        invalid_features += 1
        continue

    if label is None:
        pending += 1
        print(f"PENDING REVIEW: {recording_id} | shape={features.shape}")
        continue

    if label not in (True, False):
        pending += 1
        print(f"INVALID CORRECT LABEL: {recording_id}")
        continue

    allowed_tags = {"hand_shape", "hand_position", "hand_movement"}
    if not isinstance(tags, list) or not set(tags).issubset(allowed_tags):
        print(f"INVALID ERROR TAGS: {recording_id}")
        continue

    if label is True and tags:
        print(f"LABEL CONFLICT: correct=True but error tags exist: {recording_id}")
        continue

    ready += 1
    print(f"LABELLED FEATURE: {recording_id} | correct={label} | tags={tags}")

print("\n" + "=" * 60)
print(f"Total annotation records: {len(records)}")
print(f"Records with reviewed labels and valid features: {ready}")
print(f"Pending review: {pending}")
print(f"Missing feature files: {missing_features}")
print(f"Invalid feature files: {invalid_features}")

if ready == 0:
    print("\nSTATUS: NOT READY for supervised error-classifier training.")
    print("Next: review recordings and obtain verified labels.")
else:
    print("\nSTATUS: Some labelled records are available.")
    print("This check alone does not establish sufficient training data.")
    print("Review class counts and recording-level train/test splits.")

print("=" * 60)
