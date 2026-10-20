
"""Create sign-only landmarks using saved boundaries.

Original videos and NPZ files remain unchanged.
"""

import csv
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

ANNOTATIONS = ROOT / "dataset/annotations/pilot_sign_boundaries.csv"

SOURCE = ROOT / "dataset/processed/landmarks/pilot_hands_v1"

TARGET = ROOT / "dataset/processed/landmarks/pilot_hands_signonly_v1"

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
        rows = list(csv.DictReader(file))

    if len(rows) != 22:
        raise ValueError(
            f"Expected 22 annotations, found {len(rows)}"
        )

    # Never overwrite a previous processed dataset
    if TARGET.exists():
        raise FileExistsError(
            f"Destination already exists: {TARGET}"
        )

    jobs = []
    seen = set()

    # First validate every annotation
    for row in rows:

        video = Path(
            row["video_path"].replace("\\", "/")
        )

        signer = row["signer_id"]

        if video.parent.name != signer:
            raise ValueError(
                f"Signer mismatch: {video}"
            )

        if str(video) in seen:
            raise ValueError(
                f"Duplicate annotation: {video}"
            )

        seen.add(str(video))

        npz_path = (
            SOURCE / signer / f"{video.stem}.npz"
        )

        if not npz_path.exists():
            raise FileNotFoundError(npz_path)

        start = int(row["start_frame"])
        end = int(row["end_frame_exclusive"])

        with np.load(
            npz_path, allow_pickle=False
        ) as data:

            total = len(data["coordinates"])

            if not (0 <= start < end <= total):
                raise ValueError(
                    f"{npz_path.name}: invalid "
                    f"frames [{start}:{end}] "
                    f"for {total} frames"
                )

            if (
                str(data["sign_id"].item()) != row["sign_id"]
                or str(data["signer_id"].item()) != signer
            ):
                raise ValueError(
                    f"Metadata mismatch: {npz_path}"
                )

            for key in FRAME_KEYS:
                if (
                    key not in data
                    or len(data[key]) != total
                ):
                    raise ValueError(
                        f"Invalid frame data: {npz_path}, {key}"
                    )

        output = TARGET / signer / npz_path.name

        jobs.append((
            npz_path,
            output,
            start,
            end,
            row["annotation_status"],
        ))

    print(f"Validated {len(jobs)} videos.")

    # Create new sign-only landmark files
    for source, output, start, end, status in jobs:

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
        arrays["crop_annotation_status"] = np.array(status)

        output.parent.mkdir(
            parents=True, exist_ok=True
        )

        np.savez_compressed(output, **arrays)

        print(
            f"{output.parent.name}/{output.name}: "
            f"{end - start} frames"
        )

    print("\nDONE!")
    print("Cleaned videos:", len(jobs))
    print("Saved to:", TARGET)
    print("Original data unchanged.")
    print("Annotations still require expert review.")


if __name__ == "__main__":
    main()
