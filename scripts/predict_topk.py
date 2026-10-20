"""Export model-produced Top-3 from ordered, ALREADY SEGMENTED landmark files.

The sequence option accepts isolated sign .npz for INTEGRATION DEMOS ONLY.
These demos are not evidence of continuous-sign recognition or contextual accuracy.
"""
import argparse, json, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.recognition.preprocessing import npz_features
from src.recognition.top_k import candidates


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mode', choices=['pilot','three_signer'], default='pilot')
    p.add_argument('--model', choices=['lstm','gru','conv1d_bilstm'], required=True)
    p.add_argument('--sequence-id', required=True)
    p.add_argument('--segments', nargs='+', required=True, help='Ordered .npz files (one sign per segment)')
    p.add_argument('--out', help='Output JSON path; defaults to outputs/recognition/MODE/topk_SEQUENCE_MODEL.json')
    args=p.parse_args()
    import keras
    experiment_dir=ROOT/'outputs'/'recognition'/args.mode
    labels=json.loads((experiment_dir/'labels.json').read_text(encoding='utf-8'))
    config=json.loads((experiment_dir/'experiment.json').read_text(encoding='utf-8'))
    paths=[Path(s) if Path(s).is_absolute() else ROOT/s for s in args.segments]
    X=np.stack([npz_features(p, config['frames']) for p in paths]).astype('float32')
    m=keras.models.load_model(experiment_dir/args.model/'model.keras', compile=False)
    probs=m.predict(X,verbose=0)
    payload={
        'sequence_id': args.sequence_id, 'model_id': args.model,
        'score_type':'softmax_probability_uncalibrated',
        'segmentation': 'provided_individual_segments_not_continuous_detection',
        'evaluation_eligible': False,
        'positions':[
            {'position':i, 'source_npz':str(path), 'candidates':candidates(p,labels,3)}
            for i,(path,p) in enumerate(zip(paths,probs))
        ]
    }
    target=Path(args.out) if args.out else experiment_dir/f'topk_{args.sequence_id}_{args.model}.json'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(payload,ensure_ascii=False,indent=2), encoding='utf-8')
    print(f'Created {target}')
    for x in payload['positions']:
        print(x['position'], ' -> ', ', '.join(f"{c['sign_id']} {c['score']:.3f}" for c in x['candidates']))

if __name__ == '__main__': main()
