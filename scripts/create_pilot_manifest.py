import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIDEO_FOLDER = ROOT / "dataset" / "raw" / "expert_reference"
OUTPUT = ROOT / "dataset" / "metadata" / "pilot_video_manifest.csv"


def main():
    if not VIDEO_FOLDER.is_dir():
        raise FileNotFoundError(
            f"Video folder not found:\n{VIDEO_FOLDER}"
        )

    videos = sorted(
        path
        for path in VIDEO_FOLDER.rglob("*")
        if path.is_file() and path.suffix.lower() == ".mp4"
    )

    if not videos:
        raise RuntimeError("No MP4 videos found.")

    rows = []
    labels_by_id = {}

    for video in videos:
        # Expected filename example: S11_brother.mp4
        match = re.fullmatch(r"(S\d+)_(.+)", video.stem)

        if match is None:
            raise ValueError(
                f"Unexpected filename: {video.name}\n"
                "Expected a name such as S11_brother.mp4."
            )

        sign_id, label = match.groups()
        signer_id = video.parent.name

        if not re.fullmatch(r"expert_\d+", signer_id):
            raise ValueError(
                f"Unexpected signer folder: {signer_id}"
            )

        previous_label = labels_by_id.setdefault(sign_id, label)
        if previous_label != label:
            raise ValueError(
                f"Conflicting labels for {sign_id}: "
                f"{previous_label} and {label}"
            )

        rows.append({
            "video_path": video.relative_to(ROOT).as_posix(),
            "sign_id": sign_id,
            "label": label,
            "signer_id": signer_id,
            "label_status": "needs_review",
        })

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    # Avoid overwriting any labels you have already reviewed.
    if OUTPUT.exists():
        raise FileExistsError(
            f"CSV already exists:\n{OUTPUT}\n"
            "It has been kept unchanged."
        )

    fields = [
        "video_path",
        "sign_id",
        "label",
        "signer_id",
        "label_status",
    ]

    with OUTPUT.open("x", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Created: {OUTPUT}")
    print(f"Total videos: {len(rows)}")
    print(f"Unique sign IDs: {len(labels_by_id)}")

    for signer, count in sorted(
        Counter(row["signer_id"] for row in rows).items()
    ):
        print(f"{signer}: {count} videos")

    print("\nLabels were read from filenames.")
    print("Review them against the videos with your expert.")
    print("No videos were modified.")


if __name__ == "__main__":
    main()