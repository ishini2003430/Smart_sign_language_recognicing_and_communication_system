
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

    if not MANIFEST.is_file():
        raise FileNotFoundError(MANIFEST)

    # Read only Expert 04 records
    with MANIFEST.open(
        newline="", encoding="utf-8-sig"
    ) as file:
        rows = [
            row
            for row in csv.DictReader(file)
            if row["signer_id"] == "expert_04"
        ]

    print("Expert 04 videos found:", len(rows))

    if len(rows) != 32:
        raise ValueError(
            "Expected 32 Expert 04 videos. "
            "Check the manifest before extraction."
        )

    # Verify input videos
    for row in rows:
        video_path = ROOT / row["video_path"]

        if not video_path.is_file():
            raise FileNotFoundError(video_path)

    OUTPUT.mkdir(parents=True, exist_ok=True)

    # Keep the Expert 04 report separate
    report_path = (
        OUTPUT / "extraction_report_expert04.csv"
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
                / "expert_04"
                / f"{video_path.stem}.npz"
            )

            print(
                f"\n[{index}/{len(rows)}] "
                f"{video_path.name}"
            )

            # Never overwrite existing landmarks
            if output_path.exists():
                print("Already exists - skipped")
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
    print("Expert 04 landmarks saved to:")
    print(OUTPUT / "expert_04")
    print("Report saved to:")
    print(report_path)
    print("Expert 01/02/03 files unchanged.")


if __name__ == "__main__":
    main()
