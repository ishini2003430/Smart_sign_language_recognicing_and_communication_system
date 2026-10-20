
from pathlib import Path
import csv
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
FEATURE_ROOT = ROOT / "dataset" / "processed" / "features"
OUTPUT = ROOT / "dataset" / "splits" / "expert_split_manifest.csv"

TRAIN_EXPERTS = {"expert_01", "expert_02", "expert_03"}
TEST_EXPERT = "expert_04"

rows = []

for expert in sorted(TRAIN_EXPERTS | {TEST_EXPERT}):
    expert_dir = FEATURE_ROOT / expert

    if not expert_dir.exists():
        print(f"WARNING: Missing folder: {expert_dir}")
        continue

    split = "train_reference" if expert in TRAIN_EXPERTS else "test_unseen_expert"

    for path in sorted(expert_dir.rglob("*.npy")):
        try:
            features = np.load(path, allow_pickle=False)

            valid = (
                features.ndim == 2
                and features.shape[1] == 225
                and features.shape[0] > 0
                and np.isfinite(features).all()
            )

            rows.append({
                "expert": expert,
                "split": split,
                "sign_id": path.stem.split("_")[0].upper(),
                "filename": path.name,
                "relative_path": str(path.relative_to(ROOT)),
                "frames": features.shape[0] if features.ndim == 2 else 0,
                "feature_count": features.shape[1] if features.ndim == 2 else 0,
                "valid": valid,
            })

        except Exception as exc:
            print(f"ERROR: {path}: {exc}")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

columns = [
    "expert", "split", "sign_id", "filename",
    "relative_path", "frames", "feature_count", "valid"
]

with OUTPUT.open("w", newline="", encoding="utf-8-sig") as file:
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)

print("\n=== EXPERT DATASET SPLIT REPORT ===")
for expert in sorted(TRAIN_EXPERTS | {TEST_EXPERT}):
    items = [r for r in rows if r["expert"] == expert]
    valid_count = sum(r["valid"] for r in items)
    print(f"{expert}: {len(items)} files, {valid_count} valid")

train_signs = {
    r["sign_id"] for r in rows
    if r["split"] == "train_reference" and r["valid"]
}
test_signs = {
    r["sign_id"] for r in rows
    if r["split"] == "test_unseen_expert" and r["valid"]
}

print(f"\nTraining/reference signs: {len(train_signs)}")
print(f"Expert 4 test signs: {len(test_signs)}")
print(f"Signs covered in both: {len(train_signs & test_signs)}")
print(f"Signs missing from training references: {sorted(test_signs - train_signs)}")
print(f"Invalid feature files: {sum(not r['valid'] for r in rows)}")
print(f"\nManifest saved to: {OUTPUT.relative_to(ROOT)}")
