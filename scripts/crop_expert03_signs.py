
import csv
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

ANNOTATIONS = (
    ROOT / "dataset/annotations/pilot_sign_boundaries.csv"
)

SOURCE = (
    ROOT / "dataset/processed/landmarks/pilot_hands_v1"
)

TARGET = (
    ROOT / "dataset/processed/landmarks/pilot_hands_signonly_v1"
)

FRAME_KEYS = (
    "coordinates",
    "detected",
    "handedness_scores",
    "timestamps_ms",
)


def main():

    with ANNOTATIONS.open(
        newline="", encoding="utf-8-sig"
    ) as file:

        rows = [
            row for row in csv.DictReader(file)
            if row["signer_id"] == "expert_03"
        ]

    print("Expert 03 annotations:", len(rows))

    if len(rows) != 32:
        raise ValueError(
            "Expected 32 Expert 03 annotations."
        )

    jobs = []
    seen = set()

    # Validate all files before creating outputs
    for row in rows:

        video = Path(
            row["video_path"].replace("\\", "/")
        )

        if row["video_path"] in seen:
            raise ValueError(
                f"Duplicate annotation: {video}"
            )

        seen.add(row["video_path"])

        source = (
            SOURCE / "expert_03" / f"{video.stem}.npz"
        )

        target = (
            TARGET / "expert_03" / f"{video.stem}.npz"
        )

        if not source.is_file():
            raise FileNotFoundError(source)

        start = int(row["start_frame"])
        end = int(row["end_frame_exclusive"])

        with np.load(
            source, allow_pickle=False
        ) as data:

            total = len(data["coordinates"])

            if not (0 <= start < end <= total):
                raise ValueError(
                    f"Invalid frames for {video.name}: "
                    f"{start}:{end} / {total}"
                )

            if (
                str(data["sign_id"].item())
                != row["sign_id"]
            ):
                raise ValueError(
                    f"Sign ID mismatch: {video.name}"
                )

            for key in FRAME_KEYS:
                if key not in data or len(data[key]) != total:
                    raise ValueError(
                        f"Invalid {key}: {video.name}"
                    )

        jobs.append((source, target, start, end))

    print("All annotations validated!")

    created = 0
    skipped = 0

    for source, target, start, end in jobs:

        if target.exists():
            print("Already exists, skipping:", target.name)
            skipped += 1
            continue

        with np.load(
            source, allow_pickle=False
        ) as data:

            arrays = {}

            for key in data.files:
                value = data[key]

                if key in FRAME_KEYS:
                    arrays[key] = value[start:end].copy()
                else:
                    arrays[key] = value.copy()

        arrays["crop_start_frame"] = np.int64(start)
        arrays["crop_end_frame_exclusive"] = np.int64(end)

        target.parent.mkdir(
            parents=True, exist_ok=True
        )

        np.savez_compressed(target, **arrays)

        coverage = (
            arrays["detected"].any(axis=1).mean() * 100
        )

        print(
            f"{target.name}: "
            f"{end - start} frames | "
            f"Hand coverage: {coverage:.1f}%"
        )

        if coverage < 60:
            print("  WARNING: Low hand coverage — review needed")

        created += 1

    print("\nDONE!")
    print("Created:", created)
    print("Already existed:", skipped)
    print("Expert 03 files available:", created + skipped)
    print("Saved to:", TARGET / "expert_03")
    print("Expert 01/02 unchanged.")


if __name__ == "__main__":
    main()
