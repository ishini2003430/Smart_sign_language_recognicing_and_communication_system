import os
import sys
import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

# Ensure models/learner_feedback can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.learner_feedback.feedback_generator import generate_bilingual_feedback

FEATURES_DIR = r"dataset\processed\features"

def resolve_feature_file(expert_folder, sign_id):
    folder_path = os.path.join(FEATURES_DIR, expert_folder)
    if not os.path.exists(folder_path):
        return None

    candidates = [
        os.path.join(folder_path, f"{sign_id}.npy"),
        os.path.join(folder_path, f"{expert_folder}_{sign_id}.npy")
    ]

    for path in candidates:
        if os.path.exists(path):
            return path

    return None

def evaluate_learner_sign(learner_sequence, sign_id):
    exp1_path = resolve_feature_file("expert_01", sign_id)
    exp2_path = resolve_feature_file("expert_02", sign_id)

    if exp1_path is None and exp2_path is None:
        raise FileNotFoundError(f"No expert feature reference found for sign '{sign_id}'.")

    distances = []
    
    if exp1_path:
        exp1 = np.load(exp1_path)
        dist_1, _ = fastdtw(learner_sequence, exp1, dist=euclidean)
        distances.append(("expert_01", dist_1))

    if exp2_path:
        exp2 = np.load(exp2_path)
        dist_2, _ = fastdtw(learner_sequence, exp2, dist=euclidean)
        distances.append(("expert_02", dist_2))

    selected_expert, best_distance = min(distances, key=lambda x: x[1])

    max_threshold = 500.0  
    correctness_score = max(0.0, min(100.0, (1.0 - (best_distance / max_threshold)) * 100))
    correctness_score = round(correctness_score, 2)

    is_correct = correctness_score >= 75.0
    detected_errors = []

    if not is_correct:
        detected_errors.append("hand_shape_error")
        detected_errors.append("hand_position_error")

    feedback = generate_bilingual_feedback(detected_errors, correctness_score)

    return {
        "sign_id": sign_id,
        "matched_expert": selected_expert,
        "correctness_score": correctness_score,
        "is_correct": is_correct,
        "errors": detected_errors,
        "feedback": feedback
    }

if __name__ == "__main__":
    test_sign = "S01_amma"
    sample_file = resolve_feature_file("expert_01", test_sign)
    
    if sample_file:
        sample_input = np.load(sample_file)
        result = evaluate_learner_sign(sample_input, test_sign)
        print("\n--- Evaluation Result with Feedback ---")
        print(result)