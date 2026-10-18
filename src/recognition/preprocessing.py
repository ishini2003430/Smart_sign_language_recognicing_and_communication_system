"""V1 pilot hand-landmarks -> 48 x 134 numerical features.

Each frame: wrist-relative joint coordinates (2*21*3), global wrist positions
(2*3), and two presence flags. A fixed frame count keeps architectures fair.
No labels, signer identities, or recording names are used as model features.
"""
from pathlib import Path
import numpy as np

FRAMES = 48
FEATURE_DIM = (2 * 21 * 3) + (2 * 3) + 2


def npz_features(npz_file: str | Path, frames: int = FRAMES) -> np.ndarray:
    """Process original pilot_hands_v1 .npz (one isolated sign)."""
    with np.load(npz_file, allow_pickle=False) as data:
        if 'coordinates' not in data or 'detected' not in data:
            raise ValueError(f'{npz_file}: expected v1 coordinates/detected keys; v2 needs an explicit adapter')
        xyz = np.asarray(data['coordinates'], dtype=np.float32).copy()
        detected = np.asarray(data['detected'], dtype=bool).copy()
        if 'slot_order' in data and list(data['slot_order']) != ['Left', 'Right']:
            raise ValueError(f'{npz_file}: unexpected hand slot ordering')
    if xyz.ndim != 4 or xyz.shape[1:] != (2, 21, 3):
        raise ValueError(f'{npz_file}: invalid coordinate shape {xyz.shape}')
    if detected.shape != xyz.shape[:2] or xyz.shape[0] == 0:
        raise ValueError(f'{npz_file}: invalid detected mask / empty frames')
    # Empty detections are zeroed. Do not infer nonexistent hands.
    xyz[~detected] = 0
    xyz = np.nan_to_num(xyz, nan=0.0, posinf=0.0, neginf=0.0)
    wrist = xyz[:, :, 0, :].copy()            # (T, 2, 3)
    relative = xyz - wrist[:, :, None, :]    # shape/motion within each hand
    relative[~detected] = 0
    # Include wrist location to preserve face/chest vs other sign positions.
    features = np.concatenate([
        relative.reshape(len(xyz), -1),
        wrist.reshape(len(xyz), -1),
        detected.astype(np.float32),
    ], axis=1)
    if features.shape[1] != FEATURE_DIM:
        raise AssertionError(features.shape)
    # Simple resampling shared across models. No temporal padding leaks.
    indices = np.rint(np.linspace(0, len(features) - 1, frames)).astype(int)
    result = features[indices].astype(np.float32)
    if not np.isfinite(result).all():
        raise ValueError(f'{npz_file}: nonfinite features')
    return result
