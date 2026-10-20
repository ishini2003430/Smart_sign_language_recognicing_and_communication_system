
import argparse
import csv
from pathlib import Path

import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean


ROOT = Path(__file__).resolve().parent.parent
FEATURE_DIR = ROOT / "dataset" / "processed" / "features"
OUTPUT_DIR = ROOT / "dataset" / "processed" / "comparison_results"

EPS = 1e-8

CATEGORY_CONFIG = {
    "shape_distance": {
        "label": "Hand shape",
        "output": "hand_shape_error_score_percent",
    },
    "position_distance": {
        "label": "Hand position",
        "output": "hand_position_error_score_percent",
    },
    "movement_distance": {
        "label": "Hand movement",
        "output": "hand_movement_error_score_percent",
    },
}


def load_sequence(path):
    """Load and validate a feature sequence with 225 features per frame."""
    seq = np.load(path, allow_pickle=False).astype(np.float64)

    if seq.ndim != 2 or seq.shape[1] != 225 or len(seq) == 0:
        raise ValueError(
            f"Expected a non-empty (frames, 225) array: {path}"
        )

    if not np.isfinite(seq).all():
        raise ValueError(f"Non-finite values found in {path}")

    return seq


def landmark_blocks(frame):
    """Split a frame into left hand, right hand and pose landmarks."""
    left = frame[0:63].reshape(21, 3)
    right = frame[63:126].reshape(21, 3)
    pose = frame[126:225].reshape(33, 3)
    return left, right, pose


def hand_detected(hand):
    """Missing hands are represented by all-zero landmarks."""
    return np.any(np.abs(hand) > EPS)


def normalize_hand_shape(hand):
    """Represent hand shape relative to the wrist and hand size."""
    if not hand_detected(hand):
        return None

    points = hand.reshape(21, 3).copy()
    points -= points[0]

    # Normalize using wrist-to-middle-finger-MCP distance.
    scale = np.linalg.norm(points[9])

    if scale < EPS:
        scale = np.linalg.norm(points, axis=1).max()

    if scale < EPS:
        return None

    return points / scale


def normalize_hand_position(hand, pose):
    """Represent wrist position relative to torso and shoulder width."""
    if not hand_detected(hand):
        return None

    body = pose.reshape(33, 3)

    # MediaPipe pose landmarks 11 and 12 are the shoulders.
    left_shoulder = body[11]
    right_shoulder = body[12]

    if (
        np.linalg.norm(left_shoulder) < EPS
        or np.linalg.norm(right_shoulder) < EPS
    ):
        return None

    shoulder_width = np.linalg.norm(
        left_shoulder - right_shoulder
    )

    if shoulder_width < EPS:
        return None

    torso_center = (left_shoulder + right_shoulder) / 2.0
    wrist = hand.reshape(21, 3)[0]

    return (wrist - torso_center) / shoulder_width


def extract_categories(sequence):
    """
    Extract experimental shape, position and movement sequences.

    Movement currently represents frame-to-frame changes in wrist
    position relative to the torso. It does not fully measure
    movement direction, speed or timing.
    """
    shapes = []
    positions = []

    for frame in sequence:
        left, right, pose = landmark_blocks(frame)

        frame_shapes = []
        frame_positions = []

        for hand in (left, right):
            shape = normalize_hand_shape(hand)
            position = normalize_hand_position(hand, pose)

            if shape is not None:
                frame_shapes.append(shape.flatten())

            if position is not None:
                frame_positions.append(position.flatten())

        # Average detected hands. This is experimental and may hide
        # differences between left-hand and right-hand roles.
        shapes.append(
            np.mean(frame_shapes, axis=0)
            if frame_shapes else None
        )

        positions.append(
            np.mean(frame_positions, axis=0)
            if frame_positions else None
        )

    movements = []

    for i in range(1, len(positions)):
        if positions[i] is not None and positions[i - 1] is not None:
            movements.append(positions[i] - positions[i - 1])
        else:
            movements.append(None)

    return shapes, positions, movements


def dtw_mean_distance(a, b):
    """Calculate DTW distance averaged over the alignment path."""
    if len(a) < 2 or len(b) < 2:
        return float("nan")

    distance, path = fastdtw(a, b, dist=euclidean)

    if not path:
        return float("nan")

    return float(distance / len(path))


def compare_category(a, b):
    """Compare valid category frames, excluding missing detections."""
    a = [x for x in a if x is not None]
    b = [x for x in b if x is not None]

    if len(a) < 2 or len(b) < 2:
        return float("nan")

    return dtw_mean_distance(a, b)


def find_expert_files(sign):
    """Find the matching sign feature file for every available expert."""
    files = []

    for expert_dir in sorted(FEATURE_DIR.glob("expert_*")):
        if not expert_dir.is_dir():
            continue

        matches = sorted(
            path
            for path in expert_dir.glob(f"{sign}*.npy")
            if path.is_file()
        )

        for path in matches:
            files.append((expert_dir.name, path))

    return files


def experimental_score_from_distance(distance):
    """
    Convert a DTW distance into an experimental 0-100 score.

    IMPORTANT:
    This formula is not calibrated against human-reviewed labels.
    The result is NOT a validated percentage of actual signing errors.
    """
    if not np.isfinite(distance):
        return float("nan")

    return float(100.0 * (1.0 - np.exp(-distance)))


def summarize_category(results, distance_key):
    """
    Combine distances from the available expert references.

    First average valid expert distances, then convert the mean using
    the experimental score formula.
    """
    distances = [
        row[distance_key]
        for row in results
        if np.isfinite(row[distance_key])
    ]

    if not distances:
        return {
            "expert_count": 0,
            "mean_distance": float("nan"),
            "score_percent": float("nan"),
        }

    mean_distance = float(np.mean(distances))

    return {
        "expert_count": len(distances),
        "mean_distance": mean_distance,
        "score_percent": experimental_score_from_distance(mean_distance),
    }


def format_number(value, decimals=6):
    if not np.isfinite(value):
        return "N/A"
    return f"{value:.{decimals}f}"


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Compare one learner sequence against all available expert "
            "references using experimental three-category DTW distances."
        )
    )

    parser.add_argument(
        "--sign",
        required=True,
        help="Sign ID, for example S02",
    )
    parser.add_argument(
        "--learner",
        required=True,
        help="Path to the learner .npy feature sequence",
    )

    args = parser.parse_args()

    learner_path = Path(args.learner)

    if not learner_path.is_absolute():
        learner_path = ROOT / learner_path

    if not learner_path.is_file():
        raise FileNotFoundError(
            f"Learner feature file not found: {learner_path}"
        )

    expert_files = find_expert_files(args.sign)

    if not expert_files:
        raise FileNotFoundError(
            f"No expert feature files found for {args.sign} "
            f"under {FEATURE_DIR}"
        )

    learner_seq = load_sequence(learner_path)
    learner_categories = extract_categories(learner_seq)

    results = []

    for expert_name, expert_path in expert_files:
        expert_seq = load_sequence(expert_path)
        expert_categories = extract_categories(expert_seq)

        results.append({
            "expert": expert_name,
            "expert_file": str(expert_path.relative_to(ROOT)),
            "shape_distance": compare_category(
                learner_categories[0], expert_categories[0]
            ),
            "position_distance": compare_category(
                learner_categories[1], expert_categories[1]
            ),
            "movement_distance": compare_category(
                learner_categories[2], expert_categories[2]
            ),
            "learner_frames": len(learner_seq),
            "expert_frames": len(expert_seq),
        })

    # Produce one combined experimental score per category.
    summaries = {
        key: summarize_category(results, key)
        for key in CATEGORY_CONFIG
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Save detailed learner-vs-expert results.
    detailed_path = (
        OUTPUT_DIR / f"{args.sign}_three_category_comparison.csv"
    )

    detailed_fields = [
        "expert",
        "expert_file",
        "shape_distance",
        "position_distance",
        "movement_distance",
        "learner_frames",
        "expert_frames",
    ]

    with detailed_path.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=detailed_fields)
        writer.writeheader()
        writer.writerows(results)

    # Save one combined result per error category.
    summary_path = (
        OUTPUT_DIR / f"{args.sign}_combined_error_scores.csv"
    )

    summary_fields = [
        "sign",
        "learner_file",
        "category",
        "valid_expert_count",
        "mean_dtw_distance",
        "experimental_error_score_percent",
        "score_status",
    ]

    with summary_path.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=summary_fields)
        writer.writeheader()

        for key, config in CATEGORY_CONFIG.items():
            summary = summaries[key]
            score = summary["score_percent"]

            writer.writerow({
                "sign": args.sign,
                "learner_file": str(learner_path.relative_to(ROOT)),
                "category": config["label"],
                "valid_expert_count": summary["expert_count"],
                "mean_dtw_distance": format_number(
                    summary["mean_distance"]
                ),
                "experimental_error_score_percent": (
                    format_number(score, 2)
                    if np.isfinite(score) else "N/A"
                ),
                "score_status": (
                    "EXPERIMENTAL_NOT_VALIDATED"
                    if np.isfinite(score)
                    else "INSUFFICIENT_VALID_DATA"
                ),
            })

    # Print detailed comparison results.
    print("\n=== LEARNER vs EACH EXPERT ===")
    print(f"Sign: {args.sign}")
    print(f"Learner file: {learner_path}")
    print(f"Learner frames: {len(learner_seq)}")
    print(f"Expert recordings compared: {len(results)}")

    for row in results:
        print(f"\nLearner vs {row['expert']}")
        print(f"  Expert file: {row['expert_file']}")

        for key, label in [
            ("shape_distance", "Hand shape distance"),
            ("position_distance", "Hand position distance"),
            ("movement_distance", "Hand movement distance"),
        ]:
            print(f"  {label}: {format_number(row[key])}")

    # Print the combined three-category summary.
    print("\n=== COMBINED THREE-CATEGORY SCORES ===")
    print("Combined using the mean distance across valid expert references.")

    for key, config in CATEGORY_CONFIG.items():
        summary = summaries[key]

        print(f"\n{config['label']}:")
        print(f"  Valid expert comparisons: {summary['expert_count']}")
        print(f"  Mean DTW distance: {format_number(summary['mean_distance'])}")

        if np.isfinite(summary["score_percent"]):
            print(
                "  Experimental error score: "
                f"{summary['score_percent']:.2f}%"
            )
        else:
            print("  Experimental error score: N/A")

    print(f"\nDetailed results saved to: {detailed_path}")
    print(f"Combined scores saved to: {summary_path}")

    print(
        "\nIMPORTANT: These percentages are experimental distance-based "
        "scores, not validated error rates or model confidence. "
        "The formula must be calibrated against human-reviewed learner "
        "examples before the values can be interpreted as actual error "
        "percentages. The three categories are not directly comparable."
    )


if __name__ == "__main__":
    main()
