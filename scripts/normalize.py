import numpy as np

def normalize_landmarks(frame_vector):
    """
    Inputs:
        frame_vector: numpy array of shape (225,)
                      [Left Hand (63), Right Hand (63), Pose (99)]
    Returns:
        norm_lh, norm_rh, lh_pos_rel, rh_pos_rel
    """
    lh = frame_vector[0:63].reshape(21, 3)
    rh = frame_vector[63:126].reshape(21, 3)
    pose = frame_vector[126:225].reshape(33, 3)

    # Wrist anchors (Landmark index 0)
    lh_wrist = lh[0] if np.any(lh) else None
    rh_wrist = rh[0] if np.any(rh) else None

    # Shoulders from Pose (11: Left Shoulder, 12: Right Shoulder)
    left_shoulder = pose[11]
    right_shoulder = pose[12]
    torso_center = (left_shoulder + right_shoulder) / 2.0

    # 1. Hand Shape Normalization (Coordinates relative to wrist)
    norm_lh = (lh - lh_wrist) if lh_wrist is not None else lh
    norm_rh = (rh - rh_wrist) if rh_wrist is not None else rh

    # 2. Hand Position Normalization (Wrist relative to chest/torso)
    lh_pos_rel = (lh_wrist - torso_center) if lh_wrist is not None else np.zeros(3)
    rh_pos_rel = (rh_wrist - torso_center) if rh_wrist is not None else np.zeros(3)

    return norm_lh, norm_rh, lh_pos_rel, rh_pos_rel