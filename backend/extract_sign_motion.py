
import cv2
import json
import shutil
from pathlib import Path
import mediapipe as mp


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

VIDEO_PATH = (
    PROJECT_ROOT
    / "expert_reference"
    / "expert_reference"
    / "expert_03"
    / "S19_water.mp4"
)

OUTPUT_PATH = PROJECT_ROOT / "backend" / "water_motion.json"
BACKUP_PATH = PROJECT_ROOT / "backend" / "water_motion_backup.json"


# --------------------------------------------------
# LANDMARK CONVERSION
# --------------------------------------------------

def convert_landmarks(landmarks, include_visibility=False):
    """Convert MediaPipe landmarks to JSON-compatible dictionaries."""

    if landmarks is None:
        return []

    converted = []

    for point in landmarks.landmark:
        item = {
            "x": float(point.x),
            "y": float(point.y),
            "z": float(point.z),
        }

        if include_visibility:
            item["visibility"] = float(
                getattr(point, "visibility", 0.0)
            )

        converted.append(item)

    return converted


# --------------------------------------------------
# MAIN EXTRACTION
# --------------------------------------------------

def main():
    if not VIDEO_PATH.exists():
        raise FileNotFoundError(
            f"Reference video not found:\n{VIDEO_PATH}"
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Preserve the previous extraction before replacing it.
    if OUTPUT_PATH.exists() and not BACKUP_PATH.exists():
        shutil.copy2(OUTPUT_PATH, BACKUP_PATH)
        print(f"Previous motion data backed up to:\n{BACKUP_PATH}")

    capture = cv2.VideoCapture(str(VIDEO_PATH))

    if not capture.isOpened():
        raise RuntimeError(
            f"Could not open reference video:\n{VIDEO_PATH}"
        )

    fps = capture.get(cv2.CAP_PROP_FPS)
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    expected_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    if not fps or fps <= 0:
        fps = 30.0

    frames = []
    frame_number = 0

    pose_detected = 0
    left_hand_detected = 0
    right_hand_detected = 0
    face_detected = 0
    both_hands_detected = 0

    mp_holistic = mp.solutions.holistic

    try:
        with mp_holistic.Holistic(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            refine_face_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        ) as holistic:

            while True:
                success, image = capture.read()

                if not success:
                    break

                # Keep the original video orientation.
                # Do not flip the image automatically, because that
                # can change left/right landmark interpretation.
                rgb_image = cv2.cvtColor(
                    image,
                    cv2.COLOR_BGR2RGB
                )

                rgb_image.flags.writeable = False
                results = holistic.process(rgb_image)

                pose = convert_landmarks(
                    results.pose_landmarks,
                    include_visibility=True
                )

                left_hand = convert_landmarks(
                    results.left_hand_landmarks
                )

                right_hand = convert_landmarks(
                    results.right_hand_landmarks
                )

                face = convert_landmarks(
                    results.face_landmarks
                )

                if pose:
                    pose_detected += 1

                if left_hand:
                    left_hand_detected += 1

                if right_hand:
                    right_hand_detected += 1

                if face:
                    face_detected += 1

                if left_hand and right_hand:
                    both_hands_detected += 1

                # Keep the existing array-based frame format so
                # the current AvatarViewer can continue loading it.
                frames.append({
                    "frame_index": frame_number,
                    "time_seconds": round(
                        frame_number / fps, 5
                    ),
                    "pose": pose,
                    "left_hand": left_hand,
                    "right_hand": right_hand,
                    "face": face,
                })

                frame_number += 1

                if frame_number % 25 == 0:
                    print(
                        f"Processed {frame_number} frames..."
                    )

    finally:
        capture.release()

    if not frames:
        raise RuntimeError(
            "No frames were extracted from the reference video."
        )

    # Save to a temporary file first, then replace the output.
    temporary_path = OUTPUT_PATH.with_suffix(".tmp")

    with temporary_path.open(
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            frames,
            file,
            ensure_ascii=False,
            separators=(",", ":")
        )

    temporary_path.replace(OUTPUT_PATH)

    # --------------------------------------------------
    # VALIDATION SUMMARY
    # --------------------------------------------------

    print("\n========== EXTRACTION SUMMARY ==========")
    print(f"Video: {VIDEO_PATH.name}")
    print(f"Resolution: {width} x {height}")
    print(f"Video FPS: {fps:.2f}")
    print(f"Reported video frames: {expected_frames}")
    print(f"Processed frames: {len(frames)}")
    print(
        f"Frames with body landmarks: "
        f"{pose_detected}/{len(frames)}"
    )
    print(
        f"Frames with left-hand landmarks: "
        f"{left_hand_detected}/{len(frames)}"
    )
    print(
        f"Frames with right-hand landmarks: "
        f"{right_hand_detected}/{len(frames)}"
    )
    print(
        f"Frames with both hands: "
        f"{both_hands_detected}/{len(frames)}"
    )
    print(
        f"Frames with face landmarks: "
        f"{face_detected}/{len(frames)}"
    )
    print(f"\nOutput saved to:\n{OUTPUT_PATH}")

    print("\nLandmark counts in the first frame:")
    first_frame = frames[0]

    print(f"Pose: {len(first_frame['pose'])}")
    print(f"Left hand: {len(first_frame['left_hand'])}")
    print(f"Right hand: {len(first_frame['right_hand'])}")
    print(f"Face: {len(first_frame['face'])}")

    if pose_detected < len(frames) * 0.8:
        print(
            "\nWARNING: Body landmarks are missing in many frames."
        )

    if left_hand_detected + right_hand_detected == 0:
        print(
            "\nWARNING: No hands were detected. "
            "Check video visibility and lighting."
        )

    print(
        "\nNote: Better extraction does not guarantee correct "
        "sign animation. The avatar mapping must be calibrated "
        "and validated separately."
    )


if __name__ == "__main__":
    main()
