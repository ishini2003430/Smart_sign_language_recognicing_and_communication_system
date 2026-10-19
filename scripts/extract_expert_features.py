import os
import cv2
import numpy as np
import mediapipe as mp

# MediaPipe Task APIs
BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

# Base Directory Paths
INPUT_DIR = r"dataset\raw\expert_reference"
BASE_OUTPUT_DIR = r"dataset\processed\features"

POSE_MODEL = r"models\landmark_detectors\pose_landmarker.task"
HAND_MODEL = r"models\landmark_detectors\hand_landmarker.task"

def process_video(video_path):
    # Create fresh detectors for each video to prevent timestamp reuse errors
    pose_options = PoseLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=POSE_MODEL),
        running_mode=RunningMode.VIDEO
    )
    hand_options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=HAND_MODEL),
        running_mode=RunningMode.VIDEO,
        num_hands=2
    )

    cap = cv2.VideoCapture(video_path)
    sequence = []
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    frame_index = 0

    with PoseLandmarker.create_from_options(pose_options) as pose_detector, \
         HandLandmarker.create_from_options(hand_options) as hand_detector:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            timestamp_ms = int((frame_index / fps) * 1000)
            frame_index += 1

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

            # Detect Pose
            pose_result = pose_detector.detect_for_video(mp_image, timestamp_ms)
            if pose_result.pose_landmarks and len(pose_result.pose_landmarks) > 0:
                pose = np.array([[lm.x, lm.y, lm.z] for lm in pose_result.pose_landmarks[0]]).flatten()
            else:
                pose = np.zeros(33 * 3)

            # Detect Hands
            hand_result = hand_detector.detect_for_video(mp_image, timestamp_ms)
            lh = np.zeros(21 * 3)
            rh = np.zeros(21 * 3)

            if hand_result.hand_landmarks and hand_result.handedness:
                for hand_landmarks, handedness in zip(hand_result.hand_landmarks, hand_result.handedness):
                    label = handedness[0].category_name
                    coords = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks]).flatten()
                    if label == "Left":
                        lh = coords
                    elif label == "Right":
                        rh = coords

            frame_features = np.concatenate([lh, rh, pose])
            sequence.append(frame_features)

        cap.release()

    return np.array(sequence)

def main():
    if not os.path.exists(POSE_MODEL) or not os.path.exists(HAND_MODEL):
        raise FileNotFoundError(
            "Model files not found! Ensure 'pose_landmarker.task' and 'hand_landmarker.task' "
            "are located inside 'models/landmark_detectors/'."
        )

    for root, dirs, files in os.walk(INPUT_DIR):
        for file in files:
            if file.endswith(('.mp4', '.avi', '.mov')):
                video_path = os.path.join(root, file)
                print(f"Processing video: {video_path}")
                
                # Identify subfolder name (e.g., 'expert_01' or 'expert_02')
                folder_name = os.path.basename(root)
                
                # Create corresponding output folder: dataset/processed/features/expert_01, etc.
                target_output_dir = os.path.join(BASE_OUTPUT_DIR, folder_name)
                os.makedirs(target_output_dir, exist_ok=True)
                
                features = process_video(video_path)
                
                file_name = os.path.splitext(file)[0]
                save_name = f"{file_name}.npy"
                save_path = os.path.join(target_output_dir, save_name)
                
                np.save(save_path, features)
                print(f"Successfully saved features: {save_path} (Shape: {features.shape})")

if __name__ == "__main__":
    main()