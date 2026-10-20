
from pathlib import Path
import csv
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
FEATURE_DIR = ROOT / "dataset" / "processed" / "features" / "learner_01"
OUTPUT = ROOT / "dataset" / "processed" / "learner_feature_quality_audit.csv"


def main():
    files = sorted(FEATURE_DIR.glob("*.npy"))

    if not files:
        print("No learner feature files found:", FEATURE_DIR)
        return

    rows = []

    for path in files:
        data = np.load(path, allow_pickle=False)

        if data.ndim != 2 or data.shape[1] != 225:
            print(f"INVALID SHAPE: {path.name} -> {data.shape}")
            continue

        row = {
            "file": path.name,
            "frames": len(data),
            "finite": bool(np.isfinite(data).all()),
        }

        for name, start, end in (
            ("left", 0, 63),
            ("right", 63, 126),
            ("pose", 126, 225),
        ):
            group = data[:, start:end].reshape(len(data), -1, 3)
            landmark_present = np.any(group != 0, axis=2)
            present_pct = 100 * landmark_present.mean()

            row[f"{name}_landmark_presence_pct"] = round(
                float(present_pct), 2
            )

            if name in ("left", "right"):
                hand_present = np.any(group != 0, axis=(1, 2))
                row[f"{name}_frames_with_hand_pct"] = round(
                    float(100 * hand_present.mean()), 2
                )

        rows.append(row)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    if rows:
        with OUTPUT.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    print("\n=== LEARNER FEATURE QUALITY AUDIT ===")
    for row in rows:
        print(f"\nFile: {row['file']}")
        print(f"Frames: {row['frames']}")
        print(f"All values finite: {row['finite']}")
        print(
            f"Left hand detected in frames: "
            f"{row['left_frames_with_hand_pct']}%"
        )
        print(
            f"Right hand detected in frames: "
            f"{row['right_frames_with_hand_pct']}%"
        )
        print(
            f"Left landmark presence: "
            f"{row['left_landmark_presence_pct']}%"
        )
        print(
            f"Right landmark presence: "
            f"{row['right_landmark_presence_pct']}%"
        )
        print(
            f"Pose landmark presence: "
            f"{row['pose_landmark_presence_pct']}%"
        )

    print("\nAudit saved to:", OUTPUT)
    print("No existing feature files were modified.")


if __name__ == "__main__":
    main()

