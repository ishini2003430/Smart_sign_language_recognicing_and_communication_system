import csv
import math
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "dataset" / "metadata" / "pilot_video_manifest.csv"
MODEL = ROOT / "models" / "mediapipe" / "hand_landmarker.task"
OUTPUT = ROOT / "dataset" / "processed" / "landmarks" / "pilot_hands_v1"


def extract_video(video_path, output_path, row):
    cap = cv2.VideoCapture(str(video_path))

    try:
        if not cap.isOpened():
            raise RuntimeError(f"Cannot open video: {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        if not math.isfinite(fps) or fps <= 0:
            raise RuntimeError(f"Invalid frame rate: {video_path.name}")

        options = vision.HandLandmarkerOptions(
            base_options=python.BaseOptions(
                model_asset_path=str(MODEL)
            ),
            running_mode=vision.RunningMode.VIDEO,
            num_hands=2,
        )

        coordinates = []
        detected = []
        handedness_scores = []
        timestamps = []
        duplicate_side_frames = 0
        previous_timestamp = -1
        width = height = 0

        # A fresh detector resets tracking for each separate video.
        with vision.HandLandmarker.create_from_options(options) as detector:
            while True:
                ok, frame = cap.read()
                if not ok:
                    break

                height, width = frame.shape[:2]
                frame_index = len(coordinates)

                # Frame-rate-derived timestamps for this pilot.
                timestamp_ms = max(
                    previous_timestamp + 1,
                    round(frame_index * 1000 / fps),
                )
                previous_timestamp = timestamp_ms

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = mp.Image(
                    image_format=mp.ImageFormat.SRGB,
                    data=rgb,
                )
                result = detector.detect_for_video(image, timestamp_ms)

                # Fixed slots: 0 = predicted Left, 1 = predicted Right.
                # NaN explicitly means that coordinates are missing.
                frame_coordinates = np.full(
                    (2, 21, 3), np.nan, dtype=np.float32
                )
                frame_detected = np.zeros(2, dtype=bool)
                frame_scores = np.zeros(2, dtype=np.float32)
                duplicate_side = False

                for landmarks, categories in zip(
                    result.hand_landmarks,
                    result.handedness,
                ):
                    if not categories:
                        continue

                    category = categories[0]
                    side = category.category_name

                    if side not in ("Left", "Right"):
                        continue

                    slot = 0 if side == "Left" else 1
                    score = float(category.score)

                    # If both detections receive the same side label,
                    # keep the higher-scoring one and flag the frame.
                    if frame_detected[slot]:
                        duplicate_side = True
                        if score <= frame_scores[slot]:
                            continue

                    frame_coordinates[slot] = np.array(
                        [[point.x, point.y, point.z] for point in landmarks],
                        dtype=np.float32,
                    )
                    frame_detected[slot] = True
                    frame_scores[slot] = score

                duplicate_side_frames += int(duplicate_side)
                coordinates.append(frame_coordinates)
                detected.append(frame_detected)
                handedness_scores.append(frame_scores)
                timestamps.append(timestamp_ms)

        if not coordinates:
            raise RuntimeError(f"No readable frames: {video_path.name}")

        coordinates = np.stack(coordinates)
        detected = np.stack(detected)
        handedness_scores = np.stack(handedness_scores)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # These are extracted coordinates, not training-ready features.
        np.savez_compressed(
            output_path,
            coordinates=coordinates,
            detected=detected,
            handedness_scores=handedness_scores,
            timestamps_ms=np.asarray(timestamps, dtype=np.int64),
            fps=np.asarray(fps),
            frame_width=np.asarray(width),
            frame_height=np.asarray(height),
            video_path=np.asarray(row["video_path"]),
            sign_id=np.asarray(row["sign_id"]),
            label=np.asarray(row["label"]),
            signer_id=np.asarray(row["signer_id"]),
            label_status=np.asarray(row.get("label_status", "needs_review")),
            slot_order=np.asarray(["Left", "Right"]),
            schema_version=np.asarray("pilot_hands_v1"),
            mediapipe_version=np.asarray(mp.__version__),
        )

        total = len(coordinates)
        any_hand = int(detected.any(axis=1).sum())
        both_hands = int(detected.all(axis=1).sum())

        return {
            "video_path": row["video_path"],
            "landmark_path": output_path.relative_to(ROOT).as_posix(),
            "frames": total,
            "frames_any_hand": any_hand,
            "frames_both_hands": both_hands,
            "any_hand_percent": round(100 * any_hand / total, 2),
            "duplicate_side_frames": duplicate_side_frames,
        }

    finally:
        cap.release()


def main():
    if not MANIFEST.is_file():
        raise FileNotFoundError(f"Manifest not found: {MANIFEST}")

    if not MODEL.is_file():
        raise FileNotFoundError(f"Hand detector not found: {MODEL}")

    with MANIFEST.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        required = {"video_path", "sign_id", "label", "signer_id"}

        if not required.issubset(reader.fieldnames or []):
            raise ValueError("The manifest is missing required columns.")

        rows = list(reader)

    if not rows:
        raise RuntimeError("The manifest contains no videos.")

    jobs = []
    destinations = set()

    # Check paths before starting extraction.
    for row in rows:
        video_path = ROOT / row["video_path"]
        output_path = (
            OUTPUT / row["signer_id"] / f"{video_path.stem}.npz"
        )

        if not video_path.is_file():
            raise FileNotFoundError(f"Video missing: {video_path}")

        if output_path in destinations:
            raise ValueError(f"Duplicate output path: {output_path}")

        destinations.add(output_path)
        jobs.append((video_path, output_path, row))

    OUTPUT.mkdir(parents=True, exist_ok=True)
    report_path = OUTPUT / "extraction_report.csv"

    fields = [
        "video_path",
        "landmark_path",
        "frames",
        "frames_any_hand",
        "frames_both_hands",
        "any_hand_percent",
        "duplicate_side_frames",
    ]

    # Rerunning rebuilds only this script's generated outputs.
    with report_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for index, (video_path, output_path, row) in enumerate(jobs, 1):
            print(
                f"[{index}/{len(jobs)}] "
                f"{row['signer_id']}/{video_path.name}",
                flush=True,
            )

            summary = extract_video(video_path, output_path, row)
            writer.writerow(summary)
            file.flush()

            print(
                f"  Frames: {summary['frames']} | "
                f"Any hand: {summary['any_hand_percent']}% | "
                f"Both hands: {summary['frames_both_hands']} frames",
                flush=True,
            )

    print(f"\nFinished: {len(jobs)} videos.")
    print(f"Saved landmarks to: {OUTPUT}")
    print(f"Report: {report_path}")
    print("No sign-recognition model has been trained yet.")


if __name__ == "__main__":
    main()