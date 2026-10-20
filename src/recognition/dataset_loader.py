"""Discover pilot NPZ and create signer-isolated arrays for all models."""
from collections import defaultdict
from pathlib import Path
import numpy as np
from .preprocessing import npz_features, FRAMES


def inventory(folder: Path, allow_unreviewed: bool = False):
    if not folder.exists():
        raise FileNotFoundError(f'Landmark folder missing: {folder}')
    found = []
    rejected = []
    approved = {'approved', 'verified', 'expert_confirmed', 'reviewed'}
    for p in sorted(folder.rglob('*.npz')):
        with np.load(p, allow_pickle=False) as f:
            keys = set(f.files)
            if not {'coordinates', 'detected', 'sign_id', 'signer_id'}.issubset(keys):
                rejected.append((str(p), 'not v1 / incomplete'))
                continue
            row = dict(path=p, sign_id=str(f['sign_id'].item()),
                       signer_id=str(f['signer_id'].item()),
                       gloss=str(f['label'].item()) if 'label' in keys else str(f['sign_id'].item()),
                       status=str(f['label_status'].item()) if 'label_status' in keys else 'needs_review')
            if not allow_unreviewed and row['status'].lower() not in approved:
                rejected.append((str(p), f"unreviewed label ({row['status']})"))
                continue
            found.append(row)
    return found, rejected


def load_splits(folder: Path, mode: str, allow_unreviewed: bool, frames: int = FRAMES):
    records, rejected = inventory(folder, allow_unreviewed)
    split_signers = ({'train': ['expert_01'], 'val': [], 'test': ['expert_02']}
                     if mode == 'pilot' else
                     {'train': ['expert_01'], 'val': ['expert_02'], 'test': ['expert_03']})
    split = {}
    by_signer = defaultdict(list)
    for r in records:
        by_signer[r['signer_id']].append(r)
    missing = [s for names in split_signers.values() for s in names if s not in by_signer]
    if missing:
        raise ValueError(f'Missing signers {missing}. Found: {sorted(by_signer)}. '
                         'For current 2 signers, choose --mode pilot.')
    # Only compare shared classes; no class missing from validation/test.
    sets = []
    for names in split_signers.values():
        if names:
            sets.append({r['sign_id'] for name in names for r in by_signer[name]})
    shared_ids = sorted(set.intersection(*sets))
    if len(shared_ids) < 2:
        raise ValueError(f'Only {len(shared_ids)} common classes across signers; need >= 2.')
    dropped = [r for r in records if r['sign_id'] not in shared_ids]
    # Stable global model index based on sign_id (not arbitrary glossary order).
    label_index = {v: i for i,v in enumerate(shared_ids)}
    raw_labels = defaultdict(set)
    for r in records:
        raw_labels[r['sign_id']].add(r['gloss'])
    labels = [{'sign_id': s, 'gloss': sorted(raw_labels[s])[0]} for s in shared_ids]
    for part, names in split_signers.items():
        selected = [r for name in names for r in by_signer[name] if r['sign_id'] in label_index]
        X = np.stack([npz_features(r['path'], frames) for r in selected]) if selected else np.empty((0,frames,134), np.float32)
        y = np.array([label_index[r['sign_id']] for r in selected], dtype=np.int32)
        split[part] = (X,y,selected)
    return split, labels, rejected, dropped
