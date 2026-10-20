
import argparse
import csv
from pathlib import Path

import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean


PROJECT_ROOT = Path(__file__).resolve().parent.parent
REFERENCE_DIR = PROJECT_ROOT / "dataset" / "processed" / "reference_profiles"
FEATURE_DIR = PROJECT_ROOT / "dataset" / "processed" / "features"
RESULT_DIR = PROJECT_ROOT / "dataset" / "processed" / "comparison_results"


def load_sequence(path):
    sequence = np.load(path, allow_pickle=False)

    if sequence.ndim != 2:
        raise ValueError(f"Expected a 2D sequence: {path}")

    if sequence.shape[0] == 0 or sequence.shape[1] != 225:
        raise ValueError(
            f"Expected shape (frames, 225), got {sequence.shape}: {path}"
        )

    if not np.isfinite(sequence).all():
        raise ValueError(f"Sequence contains NaN or infinite values: {path}")

    return sequence.astype(np.float64)


def main():
    parser = argparse.ArgumentParser(
        description="Compare a learner sequence with expert DTW references."
    )
    parser.add_argument("--sign", required=True, help="Sign ID, e.g. S02")
    parser.add_argument("--learner", required=True, help="Path to learner .npy")
    args = parser.parse_args()

    learner_path = Path(args.learner)
    if not learner_path.is_absolute():
        learner_path = PROJECT_ROOT / learner_path

    profile_path = REFERENCE_DIR / f"{args.sign}.npz"

    if not learner_path.is_file():
        raise FileNotFoundError(f"Learner file not found: {learner_path}")

    if not profile_path.is_file():
        raise FileNotFoundError(f"Reference profile not found: {profile_path}")

    learner = load_sequence(learner_path)
    results = []

    with np.load(profile_path, allow_pickle=False) as profile:
        for expert_name in profile.files:
            expert = np.asarray(profile[expert_name], dtype=np.float64)

            if expert.ndim != 2 or expert.shape[1] != learner.shape[1]:
                raise ValueError(
                    f"Invalid features for {expert_name}: {expert.shape}"
                )

            distance, path = fastdtw(
                learner, expert, dist=euclidean
            )

            path_length = len(path)
            mean_path_distance = (
                distance / path_length if path_length else float("nan")
            )

            results.append({
                "expert": expert_name,
                "expert_frames": len(expert),
                "learner_frames": len(learner),
                "dtw_total_distance": float(distance),
                "dtw_mean_path_distance": float(mean_path_distance),
                "alignment_path_length": path_length,
            })

    results.sort(key=lambda row: row["dtw_mean_path_distance"])
    best = results[0]

    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RESULT_DIR / f"{args.sign}_learner_comparison.csv"

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print("\n=== DTW Learner-to-Expert Comparison ===")
    print(f"Sign: {args.sign}")
    print(f"Learner file: {learner_path}")
    print(f"Learner frames: {len(learner)}")
    print("\nResults (lower distance means a closer sequence match):")

    for row in results:
        print(
            f"{row['expert']}: "
            f"total distance={row['dtw_total_distance']:.4f}, "
            f"mean path distance={row['dtw_mean_path_distance']:.6f}"
        )

    print(f"\nClosest reference: {best['expert']}")
    print(f"Mean path distance: {best['dtw_mean_path_distance']:.6f}")
    print(f"CSV saved to: {output_path}")
    print("\nNote: These are DTW distances, NOT validated error percentages.")


if __name__ == "__main__":
    main()
