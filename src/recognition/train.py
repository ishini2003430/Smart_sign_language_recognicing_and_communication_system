"""Train equal-input baselines. 3-signer mode holds one person out for testing.

Pilot mode (2 signers) is ONLY a functionality smoke test. Its evaluation
must never be presented as final accuracy or used for model selection.
"""
import argparse, csv, json, os, random, sys
from pathlib import Path
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

from .dataset_loader import load_splits
from .preprocessing import FRAMES
from .top_k import candidates


def _serialize(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding='utf-8')


def execute(root, mode='pilot', model_name='all', epochs=5, allow_unreviewed=False, landmarks='dataset/processed/landmarks/pilot_hands_v1'):
    # Lazy import permits dataset audits when TensorFlow is not installed.
    import keras
    from .architectures import FACTORIES
    keras.utils.set_random_seed(42)
    np.random.seed(42)
    random.seed(42)
    split, labels, rejected, dropped = load_splits(root / landmarks, mode, allow_unreviewed)
    n = len(labels)
    selection = list(FACTORIES) if model_name == 'all' else [model_name]
    print(f'Classes shared by signers: {n}: {[l["sign_id"] for l in labels]}')
    for part,(X,y,rs) in split.items():
        print(f'  {part}: {len(y)} videos; signers={sorted(set(r["signer_id"] for r in rs))}')
    print(f'Dropped outside common classes: {len(dropped)}; excluded/unreviewed: {len(rejected)}')
    if mode == 'pilot':
        print('WARNING: TWO-SIGNER SMOKE TEST ONLY. No reliable model ranking or final accuracy!')
    elif len(split['train'][1]) < 5 * n:
        print('WARNING: TRAINING EXAMPLES ARE EXTREMELY FEW. Results will be unstable.')
    output_dir = root / 'outputs' / 'recognition' / mode
    output_dir.mkdir(parents=True, exist_ok=True)
    # Freeze exact file assignment to make the experiment auditable.
    with (output_dir / 'split_manifest.csv').open('w', newline='', encoding='utf-8') as fp:
        writer = csv.DictWriter(fp, fieldnames=['split','npz_path','sign_id','signer_id','label_status'])
        writer.writeheader()
        for group, (X,y,records) in split.items():
            for item in records:
                writer.writerow({'split': group, 'npz_path': item['path'].relative_to(root).as_posix(),
                                 'sign_id': item['sign_id'], 'signer_id': item['signer_id'],
                                 'label_status': item['status']})
    _serialize(output_dir / 'labels.json', labels)
    _serialize(output_dir / 'experiment.json', {
        'mode': mode, 'frames': FRAMES, 'feature_dim': 134,
        'input_schema': 'pilot_hands_v1', 'class_ids': [l['sign_id'] for l in labels],
        'allow_unreviewed': allow_unreviewed,
        'split_signers': {k: sorted({r['signer_id'] for r in v[2]}) for k,v in split.items()},
        'discarded_classes': sorted({r['sign_id'] for r in dropped}),
        'n_rejected': len(rejected),
        'purpose': 'pipeline_smoke_test_only' if mode == 'pilot' else 'limited_three_signer_preliminary_experiment',
        'caveat': 'One take per class per person is insufficient for credible generalization estimates.',
    })
    reports = []
    for name in selection:
        keras.backend.clear_session()
        keras.utils.set_random_seed(42)
        builder = FACTORIES[name]
        m = builder((FRAMES,134), n)
        m.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001),
                  loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        val_X, val_y, _ = split['val']
        has_val = len(val_y) > 0
        callbacks = []
        if has_val:
            callbacks.append(keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True))
        print(f'\nTRAINING {name} | trainable parameters={m.count_params()}')
        history = m.fit(split['train'][0], split['train'][1], batch_size=min(4,len(split['train'][1])),
                        epochs=epochs, validation_data=(val_X,val_y) if has_val else None,
                        callbacks=callbacks, verbose=2, shuffle=True)
        model_dir = output_dir / name
        model_dir.mkdir(parents=True, exist_ok=True)
        m.save(model_dir / 'model.keras')
        _serialize(model_dir / 'history.json', {k: [float(z) for z in v] for k,v in history.history.items()})
        test_X, test_y, test_records = split['test']
        probs = np.asarray(m.predict(test_X, verbose=0), dtype=float)
        pred = probs.argmax(axis=1)
        k = min(3, n)
        top_k_recall = float(np.mean([int(int(y) in np.argsort(-p)[:k]) for y,p in zip(test_y, probs)]))
        report = {'model': name, 'mode': mode,
                  'is_final_test': False, 'accuracy': float(accuracy_score(test_y, pred)),
                  'macro_f1': float(f1_score(test_y, pred, labels=np.arange(n), average='macro', zero_division=0)),
                  'top_k_recall': top_k_recall, 'k': k,
                  'n_test': len(test_y), 'n_classes': n, 'n_parameters': int(m.count_params()),
                  'evaluation_note': 'pilot smoke test only; DO NOT claim final model winner' if mode=='pilot' else 'limited signer-held-out preliminary result',
                  'score_type': 'softmax_output_not_calibrated_confidence'}
        _serialize(model_dir / 'metrics.json', report)
        _serialize(model_dir / 'confusion_matrix.json', {
            'labels': [v['sign_id'] for v in labels],
            'counts': confusion_matrix(test_y, pred, labels=np.arange(n)).tolist(),
        })
        reports.append(report)
        with (model_dir / 'topk_isolated_predictions.jsonl').open('w', encoding='utf-8') as f:
            for row, p in zip(test_records, probs):
                record = {'sequence_id': f'ISOLATED_{row["path"].stem}_{row["signer_id"]}',
                          'model_id': name, 'position': 0,
                          'score_type': 'softmax_probability_uncalibrated',
                          'input_source': 'isolated_single_sign_smoke_test',
                          'candidates': candidates(p,labels,k)}
                f.write(json.dumps(record, ensure_ascii=False)+'\n')
        print(f'Saved model and Top-{k} predictions: {model_dir}')
    _serialize(output_dir / 'comparison.json', reports)
    with (output_dir / 'comparison.csv').open('w', newline='', encoding='utf-8') as fp:
        writer=csv.DictWriter(fp,fieldnames=['model','mode','n_test','n_classes','n_parameters','accuracy','macro_f1','top_k_recall','evaluation_note'])
        writer.writeheader()
        for report in reports:writer.writerow({k:report.get(k) for k in writer.fieldnames})
    print(f'\nDONE. Outputs under {output_dir}')


def cli():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mode', choices=['pilot','three_signer'], default='pilot')
    p.add_argument('--model', choices=['all','lstm','gru','conv1d_bilstm'], default='all')
    p.add_argument('--epochs', type=int, default=5)
    p.add_argument('--allow-unreviewed', action='store_true', help='ONLY for pipeline testing on needs_review pilot labels')
    p.add_argument('--landmarks', default='dataset/processed/landmarks/pilot_hands_v1', help='path relative to repo root containing v1 .npz')
    args=p.parse_args()
    if args.epochs < 1: p.error('--epochs must be >= 1')
    root=Path(__file__).resolve().parents[2]
    execute(root, mode=args.mode, model_name=args.model, epochs=args.epochs,
            allow_unreviewed=args.allow_unreviewed, landmarks=args.landmarks)
