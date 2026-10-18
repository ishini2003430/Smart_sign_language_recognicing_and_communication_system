"""Shared model predictions -> contextual resolver candidate contract."""
import numpy as np

def candidates(probs, labels, k=3):
    probs = np.asarray(probs, dtype=float).reshape(-1)
    if probs.shape != (len(labels),):
        raise ValueError('Probability count and labels mismatch')
    ranks = np.argsort(-probs)[:min(k, len(probs))]
    return [{'rank': int(j+1), 'sign_id': labels[int(i)]['sign_id'],
             'gloss': labels[int(i)]['gloss'], 'score': float(probs[i])}
            for j, i in enumerate(ranks)]
