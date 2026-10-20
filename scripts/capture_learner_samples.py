
import csv
import re
import time
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

HAND_MODEL = (
    ROOT / "models" / "landmark_detectors" / "hand_landmarker.task"
)
POSE_MODEL = (
    ROOT / "models" / "landmark_detectors" / "pose_landmarker.task"
)

RAW_DIR = ROOT / "dataset" / "raw" / "learner_samples"
FEATURE_DIR = ROOT / "dataset" / "processed" / "features"

METADATA_FILE = (
    ROOT / "dataset" / "annotations" / "learner_capture_metadata.csv"
)

FEATURE_COUNT = 225


# ============================================================
# ALL 32 SLSL SIGN IDs
# ============================================================

SIGNS = {
    "S01": "amma",
    "S02": "father",
    "S03": "daughter",
    "S04": "go",
    "S05": "come",
    "S06": "welcome",
    "S07": "school",
    "S08": "friend",
    "S09": "sister",
    "S10": "son",
    "S11": "brother",
    "S12": "home",
    "S13": "Younger_brother",
    "S14": "Younger_Sister",
    "S15": "eat",
    "S16": "I",
    "S17": "You",
    "S18": "want",
    "S19": "water",
    "S20": "see",
    "S21": "month",
    "S22": "friday",
    "S23": "february",
    "S24": "me",
    "S25": "mine",
    "S26": "how",
    "S27": "drink",
    "S28": "why",
    "S29": "think",
    "S30": "know",
    "S31": "look",
    "S32": "colombo",
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_name(value):
    """Convert an ID into a safe folder name."""
    value = value.strip()
    value = re.sub(r"[^A-Za-z0-9_-]+", "_", value)

    if not value:
        raise ValueError("ID cannot be empty.")

    return value


def landmark_values(landmarks, count):
    """
    Return x, y, z for every landmark.
    Return zeros when landmarks are unavailable.
    """
    if not landmarks:
        return np.zeros(count * 3, dtype=np.float32)

    values = []

    for landmark in landmarks[:count]:
        values.extend([
            float(landmark.x),
            float(landmark.y),
            float(landmark.z),
        ])

    values = values[:count * 3]

    if len(values) < count * 3:
        values.extend([0.0] * (count * 3 - len(values)))

    return np.asarray(values, dtype=np.float32)


def extract_frame_features(
    image,
    hand_detector,
    pose_detector,
    timestamp_ms,
):
    """
    Extract 225 features in this order:
    left hand (63), right hand (63), pose (99).
    """
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_image,
    )

    hand_result = hand_detector.detect_for_video(
        mp_image, timestamp_ms
    )

    pose_result = pose_detector.detect_for_video(
        mp_image, timestamp_ms
    )

    left_hand = np.zeros(63, dtype=np.float32)
    right_hand = np.zeros(63, dtype=np.float32)

    detected_hands = hand_result.hand_landmarks or []
    handedness_groups = hand_result.handedness or []

    for index, hand_landmarks in enumerate(detected_hands):
        label = ""

        if (
            index < len(handedness_groups)
            and handedness_groups[index]
        ):
            label = (
                handedness_groups[index][0]
                .category_name.lower()
            )

        hand_values = landmark_values(hand_landmarks, 21)

        if label == "left":
            left_hand = hand_values
        elif label == "right":
            right_hand = hand_values

    pose_landmarks = (
        pose_result.pose_landmarks[0]
        if pose_result.pose_landmarks
        else None
    )

    pose_values = landmark_values(pose_landmarks, 33)

    features = np.concatenate([
        left_hand,
        right_hand,
        pose_values,
    ]).astype(np.float32)

    if features.shape != (FEATURE_COUNT,):
        raise ValueError(
            f"Expected {FEATURE_COUNT} features; "
            f"received {features.shape}"
        )

    return features


def create_video_writer(video_path, frame):
    """Create an MP4 writer matching the camera frame size."""
    height, width = frame.shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(
        str(video_path),
        fourcc,
        30.0,
        (width, height),
    )

    if not writer.isOpened():
        writer.release()
        raise RuntimeError(
            f"Could not create video file: {video_path}"
        )

    return writer


# ============================================================
# MAIN CAPTURE PROGRAM
# ============================================================

def main():

    # Check the model files.
    if not HAND_MODEL.exists():
        raise FileNotFoundError(
            f"Hand model not found: {HAND_MODEL}"
        )

    if not POSE_MODEL.exists():
        raise FileNotFoundError(
            f"Pose model not found: {POSE_MODEL}"
        )

    print("\n========================================")
    print(" SLSL C3 LEARNER SAMPLE CAPTURE")
    print("========================================")

    # Display all 32 signs.
    print("\nAvailable Sign IDs:\n")

    for sign_code, sign_name in SIGNS.items():
        print(
            f"  {sign_code} - "
            f"{sign_name.replace('_', ' ').title()}"
        )

    # Ask for learner ID.
    while True:
        learner_input = input(
            "\nEnter learner ID (example learner_01): "
        )

        try:
            learner_id = safe_name(learner_input)
            break
        except ValueError as error:
            print(error)

    # Ask for sign ID.
    while True:
        sign_id = input(
            "\nEnter sign ID only (example S02): "
        ).strip().upper()

        if sign_id in SIGNS:
            break

        print(
            "Invalid sign ID. "
            "Choose one of the displayed S01-S32 IDs."
        )

    sign_name = SIGNS[sign_id]
    sign_folder_name = f"{sign_id}_{sign_name}"

    print("\nSelected sign:")
    print(f"  ID:   {sign_id}")
    print(f"  Name: {sign_name.replace('_', ' ').title()}")

    # Create output directories.
    learner_video_dir = RAW_DIR / learner_id
    learner_feature_dir = FEATURE_DIR / learner_id

    learner_video_dir.mkdir(parents=True, exist_ok=True)
    learner_feature_dir.mkdir(parents=True, exist_ok=True)
    METADATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Configure MediaPipe hand detector.
    hand_options = vision.HandLandmarkerOptions(
        base_options=python.BaseOptions(
            model_asset_path=str(HAND_MODEL)
        ),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=2,
    )

    # Configure MediaPipe pose detector.
    pose_options = vision.PoseLandmarkerOptions(
        base_options=python.BaseOptions(
            model_asset_path=str(POSE_MODEL)
        ),
        running_mode=vision.RunningMode.VIDEO,
    )

    # Open webcam.
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        raise RuntimeError(
            "Could not open webcam. Close other camera apps "
            "and check that your camera is connected."
        )

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    recording = False
    writer = None
    frame_features = []

    attempt = 0
    started_at = None
    video_path = None
    feature_path = None

    # MediaPipe VIDEO timestamps must increase.
    start_clock = time.monotonic()
    last_timestamp_ms = -1

    # --------------------------------------------------------
    # SAVE ONE ATTEMPT AND RUN AUTOMATIC COMPARISON
    # --------------------------------------------------------

    def save_attempt():
        nonlocal frame_features, recording, writer

        # Release video writer before comparing.
        if writer is not None:
            writer.release()
            writer = None

        if not frame_features:
            print("No frames recorded. Nothing was saved.")
            recording = False
            return

        # Convert captured features into a sequence.
        sequence = np.stack(
            frame_features
        ).astype(np.float32)

        # Save feature sequence.
        np.save(feature_path, sequence)

        # Append metadata.
        metadata_exists = (
            METADATA_FILE.exists()
            and METADATA_FILE.stat().st_size > 0
        )

        fields = [
            "recording_id",
            "learner_id",
            "intended_form_id",
            "video_path",
            "feature_path",
            "frame_count",
            "feature_count",
            "recorded_at",
            "annotation_status",
        ]

        with METADATA_FILE.open(
            "a",
            newline="",
            encoding="utf-8",
        ) as file:

            csv_writer = csv.DictWriter(
                file,
                fieldnames=fields,
            )

            if not metadata_exists:
                csv_writer.writeheader()

            csv_writer.writerow({
                "recording_id": video_path.stem,
                "learner_id": learner_id,
                "intended_form_id": sign_folder_name,
                "video_path": str(
                    video_path.relative_to(ROOT)
                ),
                "feature_path": str(
                    feature_path.relative_to(ROOT)
                ),
                "frame_count": sequence.shape[0],
                "feature_count": sequence.shape[1],
                "recorded_at": started_at,
                "annotation_status": "pending_review",
            })

        print("\n----------------------------------------")
        print("Attempt saved successfully!")
        print("----------------------------------------")
        print(f"Sign:     {sign_id} - {sign_name}")
        print(f"Video:    {video_path}")
        print(f"Features: {feature_path}")
        print(
            f"Shape:    {sequence.shape} (frames, features)"
        )
        print(f"Metadata: {METADATA_FILE}")
        print("Label:    pending_review")
        print("----------------------------------------")

        # Reset recording state before comparison.
        frame_features = []
        recording = False

        # ----------------------------------------------------
        # AUTOMATIC C3 COMPARISON
        # ----------------------------------------------------

        print("\nStarting automatic C3 comparison...")

        comparison_script = (
            ROOT / "scripts" / "compare_three_error_categories.py"
        )

        if not comparison_script.exists():
            print(
                "Comparison script not found:\n"
                f"{comparison_script}"
            )
            return

        try:
            completed = subprocess.run(
                [
                    sys.executable,
                    str(comparison_script),
                    "--sign",
                    sign_id,
                    "--learner",
                    str(feature_path),
                ],
                cwd=str(ROOT),
                check=False,
            )

            if completed.returncode == 0:
                print("\nAutomatic C3 comparison completed.")
                print(
                    "Check the comparison_results folder "
                    "for the output CSV files."
                )
            else:
                print(
                    "\nAutomatic comparison failed. "
                    "Check the error messages above."
                )

        except Exception as error:
            print(
                f"\nCould not run automatic C3 comparison: {error}"
            )

    # --------------------------------------------------------
    # CAMERA LOOP
    # --------------------------------------------------------

    print("\nControls:")
    print("  R       = Start recording")
    print("  R again = Stop, save and compare")
    print("  Q / ESC = Save current attempt (if recording) and exit")
    print("\nKeep your hands and upper body visible.")
    print("Click the webcam window before using keyboard controls.")

    try:
        with vision.HandLandmarker.create_from_options(
            hand_options
        ) as hand_detector, vision.PoseLandmarker.create_from_options(
            pose_options
        ) as pose_detector:

            while True:
                ok, frame = camera.read()

                if not ok:
                    print("Could not read a webcam frame.")
                    break

                # Keyboard controls.
                key = cv2.waitKey(1) & 0xFF

                # Exit and save if recording.
                if key in (ord("q"), ord("Q"), 27):
                    if recording:
                        save_attempt()
                    break

                # Start or stop recording.
                if key in (ord("r"), ord("R")):

                    if not recording:
                        attempt += 1

                        timestamp = datetime.now().strftime(
                            "%Y%m%d_%H%M%S"
                        )

                        recording_id = (
                            f"{sign_folder_name}_{learner_id}_"
                            f"attempt{attempt:02d}_{timestamp}"
                        )

                        video_path = (
                            learner_video_dir
                            / f"{recording_id}.mp4"
                        )

                        feature_path = (
                            learner_feature_dir
                            / f"{recording_id}.npy"
                        )

                        started_at = datetime.now().isoformat(
                            timespec="seconds"
                        )

                        try:
                            writer = create_video_writer(
                                video_path, frame
                            )
                        except RuntimeError as error:
                            print(error)
                            continue

                        frame_features = []
                        recording = True

                        print(
                            f"\nRecording {sign_id} - {sign_name}..."
                        )

                    else:
                        # Saves the attempt and automatically
                        # runs the C3 comparison.
                        save_attempt()

                # Extract features while recording.
                if recording:
                    timestamp_ms = int(
                        (time.monotonic() - start_clock) * 1000
                    )

                    timestamp_ms = max(
                        timestamp_ms,
                        last_timestamp_ms + 1,
                    )

                    last_timestamp_ms = timestamp_ms

                    features = extract_frame_features(
                        frame,
                        hand_detector,
                        pose_detector,
                        timestamp_ms,
                    )

                    frame_features.append(features)
                    writer.write(frame)

                # Display recording status.
                display = frame.copy()

                status = (
                    "RECORDING - press R to save"
                    if recording
                    else "READY - press R to record"
                )

                status_color = (
                    (0, 0, 255)
                    if recording
                    else (0, 200, 0)
                )

                cv2.putText(
                    display,
                    status,
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    status_color,
                    2,
                )

                cv2.putText(
                    display,
                    f"Learner: {learner_id} | Sign: {sign_folder_name}",
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.50,
                    (255, 255, 255),
                    2,
                )

                cv2.putText(
                    display,
                    f"Frames: {len(frame_features)}",
                    (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (255, 255, 255),
                    2,
                )

                cv2.imshow(
                    "SLSL C3 Learner Capture",
                    display,
                )

    finally:
        if writer is not None:
            writer.release()

        camera.release()
        cv2.destroyAllWindows()

    print("\nWebcam released. Capture session finished.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCapture interrupted by user.")
        print("Check the output folders for saved recordings.")

