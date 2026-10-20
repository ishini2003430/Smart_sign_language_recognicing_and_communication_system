
import csv

from extract_pilot_hand_landmarks import (
    ROOT,
    MANIFEST,
    MODEL,
    OUTPUT,
    extract_video,
)


def main():
    if not MODEL.is_file():
        raise FileNotFoundError(MODEL)

    with MANIFEST.open(
        newline="", encoding="utf-8-sig"
    ) as file:
        rows = [
            row
            for row in csv.DictReader(file)
            if row["signer_id"] == "expert_03"
        ]

    print("Expert 03 videos found:", len(rows))

    if len(rows) != 32:
        raise ValueError(
            "Expected 32 Expert 03 videos. "
            "Check the manifest before extraction."
        )

    # Verify the input videos before extraction
    for row in rows:
        video_path = ROOT / row["video_path"]

        if not video_path.is_file():
            raise FileNotFoundError(video_path)

    OUTPUT.mkdir(parents=True, exist_ok=True)

    report_path = (
        OUTPUT / "extraction_report_expert03.csv"
    )

    columns = [
        "video_path",
        "landmark_path",
        "frames",
        "frames_any_hand",
        "frames_both_hands",
        "any_hand_percent",
        "duplicate_side_frames",
    ]

    report_exists = report_path.exists()

    with report_path.open(
        "a" if report_exists else "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file, fieldnames=columns
        )

        if not report_exists:
            writer.writeheader()

        for index, row in enumerate(rows, start=1):

            video_path = ROOT / row["video_path"]

            output_path = (
                OUTPUT
                / "expert_03"
                / f"{video_path.stem}.npz"
            )

            print(
                f"\n[{index}/{len(rows)}] "
                f"{video_path.name}"
            )

            # Preserve already-extracted files
            if output_path.exists():
                print("Already exists — skipped")
                continue

            summary = extract_video(
                video_path,
                output_path,
                row
            )

            writer.writerow(summary)
            file.flush()

            print(
                "Frames:", summary["frames"],
                "| Hand detection:",
                f"{summary['any_hand_percent']}%"
            )

    print("\nDONE!")
    print("Expert 03 landmarks saved to:")
    print(OUTPUT / "expert_03")
    print("Existing Expert 01/02 files unchanged.")


if __name__ == "__main__":
    main()
