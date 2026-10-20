"""Validate v1 landmarks exist and show signer/class coverage without TensorFlow."""
from pathlib import Path
import argparse, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.recognition.dataset_loader import inventory
from src.recognition.preprocessing import npz_features

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--landmarks',default='dataset/processed/landmarks/pilot_hands_v1')
    p.add_argument('--allow-unreviewed',action='store_true')
    a=p.parse_args()
    data,rejected=inventory(ROOT/a.landmarks,a.allow_unreviewed)
    by={}
    for row in data:
        k=row['signer_id'];by.setdefault(k,set()).add(row['sign_id'])
        arr=npz_features(row['path'])
        if arr.shape != (48,134):raise AssertionError(arr.shape)
    print(f'Usable NPZ: {len(data)}; rejected: {len(rejected)}')
    for s,labels in sorted(by.items()):print(s,len(labels),sorted(labels))
    if rejected:print('Rejected (first 5):',rejected[:5])

if __name__=='__main__':main()
