
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent

EXPERT_DIR = ROOT / "dataset" / "processed" / "features"
LEARNER_DIR = ROOT / "dataset" / "processed" / "features"

FEATURE_COUNT = 225

def inspect_file(path):
    data = np.load(path, allow_pickle=False)

    print(f"\nFile: {path.relative_to(ROOT)}")
    print(f"Shape: {data.shape}")

    if data.ndim != 2 or data.shape[1] != FEATURE_COUNT:
        print("STATUS: INVALID FEATURE SHAPE")
        return

    print(f"Finite values: {np.isfinite(data).all()}")

    groups = {
        "Left hand": data[:, 0:63],
        "Right hand": data[:, 63:126],
        "Pose": data[:, 126:225],
    }

    for name, group in groups.items():
        # A landmark is missing if its x, y and z are all zero.
        landmarks = group.reshape(len(data), -1, 3)
        missing = np.all(landmarks == 0, axis=2)
        missing_pct = 100 * missing.mean()

        print(f"{name} missing landmark values: {missing_pct:.2f}%")

    print("STATUS: Valid array shape")

def main():
    print("=== Expert feature examples ===")

    for expert in ("expert_01", "expert_02", "expert_03", "expert_04"):
        folder = EXPERT_DIR / expert
        files = sorted(folder.glob("*.npy")) if folder.exists() else []

        print(f"\n{expert}: {len(files)} files")

        for path in files[:2]:
            inspect_file(path)

    print("\n=== Learner feature examples ===")

    learner_root = LEARNER_DIR / "learner_01"
    files = sorted(learner_root.glob("*.npy")) if learner_root.exists() else []

    print(f"Learner files: {len(files)}")

    for path in files[-3:]:
        inspect_file(path)

if __name__ == "__main__":
    main()
