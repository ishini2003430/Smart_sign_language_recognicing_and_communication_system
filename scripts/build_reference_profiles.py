
from pathlib import Path
import json
import csv
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
FEATURE_ROOT = ROOT / "dataset" / "processed" / "features"
OUTPUT_DIR = ROOT / "dataset" / "processed" / "reference_profiles"
SUMMARY_CSV = OUTPUT_DIR / "reference_profile_summary.csv"
METADATA_JSON = OUTPUT_DIR / "reference_profile_metadata.json"

# Only these experts are permitted to build reference profiles.
TRAIN_EXPERTS = ["expert_01", "expert_02", "expert_03"]
EXPECTED_FEATURES = 225

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

profiles = {}
summary_rows = []
errors = []

for expert in TRAIN_EXPERTS:
    expert_dir = FEATURE_ROOT / expert

    if not expert_dir.exists():
        errors.append(f"Missing expert directory: {expert_dir}")
        continue

    for path in sorted(expert_dir.rglob("*.npy")):
        # The sign ID is the first part of the filename, e.g. S05_come -> S05.
        sign_id = path.stem.split("_")[0].upper()

        try:
            sequence = np.load(path, allow_pickle=False)

            if sequence.ndim != 2:
                raise ValueError(f"Expected 2D array, got {sequence.shape}")

            if sequence.shape[1] != EXPECTED_FEATURES:
                raise ValueError(
                    f"Expected {EXPECTED_FEATURES} features, got {sequence.shape}"
                )

            if sequence.shape[0] == 0 or not np.isfinite(sequence).all():
                raise ValueError("Empty sequence or non-finite feature values")

            profiles.setdefault(sign_id, {})[expert] = sequence

            summary_rows.append({
                "sign_id": sign_id,
                "expert": expert,
                "source_file": str(path.relative_to(ROOT)),
                "frames": sequence.shape[0],
                "feature_count": sequence.shape[1],
                "valid": True,
            })

        except Exception as exc:
            errors.append(f"{path}: {exc}")

# Stop if any source files are invalid; don't silently build incomplete profiles.
if errors:
    print("ERROR: Reference profiles were not written.")
    for error in errors:
        print(" -", error)
    raise SystemExit(1)

# One compressed file per sign. Each expert sequence remains separate.
for sign_id, expert_sequences in sorted(profiles.items()):
    output_path = OUTPUT_DIR / f"{sign_id}.npz"
    np.savez_compressed(output_path, **expert_sequences)

metadata = {
    "purpose": "DTW expert reference sequences for C3",
    "training_experts": TRAIN_EXPERTS,
    "excluded_test_expert": "expert_04",
    "feature_count": EXPECTED_FEATURES,
    "method": "Preserve individual variable-length expert sequences; no frame averaging",
    "profiles": {
        sign_id: {
            "file": f"{sign_id}.npz",
            "experts_included": sorted(expert_sequences.keys()),
            "sequence_count": len(expert_sequences),
        }
        for sign_id, expert_sequences in sorted(profiles.items())
    },
}

METADATA_JSON.write_text(
    json.dumps(metadata, indent=2),
    encoding="utf-8"
)

with SUMMARY_CSV.open("w", newline="", encoding="utf-8-sig") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "sign_id", "expert", "source_file",
            "frames", "feature_count", "valid"
        ]
    )
    writer.writeheader()
    writer.writerows(summary_rows)

print("\n=== REFERENCE PROFILE BUILD REPORT ===")
print("Training experts:", ", ".join(TRAIN_EXPERTS))
print("Held-out expert: expert_04 (excluded)")
print("Valid source sequences:", len(summary_rows))
print("Unique signs:", len(profiles))
print("Profile files written:", len(profiles))

for sign_id, expert_sequences in sorted(profiles.items()):
    frame_info = ", ".join(
        f"{expert}={seq.shape[0]} frames"
        for expert, seq in sorted(expert_sequences.items())
    )
    print(f"{sign_id}: {frame_info}")

print("\nSaved to:", OUTPUT_DIR.relative_to(ROOT))
print("Summary:", SUMMARY_CSV.relative_to(ROOT))
print("Metadata:", METADATA_JSON.relative_to(ROOT))
