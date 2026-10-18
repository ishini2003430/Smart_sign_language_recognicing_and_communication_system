# SLSL Recognition — LSTM, GRU, Conv1D + BiLSTM (PP1 starter)

**Adds functioning files to the existing repository rather than creating a second project.**

## What this implements
- `src/recognition/preprocessing.py`: 48-frame fixed-length representation of the existing `pilot_hands_v1` NPZ files (134 features per frame).
- `src/recognition/architectures/{lstm,gru,conv1d_bilstm}.py`: small TensorFlow-backed Keras models.
- `src/recognition/dataset_loader.py`: reads `sign_id` and `signer_id` from the NPZ files and uses identical class ordering across models.
- `scripts/check_landmarks.py`: inspect class coverage; no TensorFlow needed.
- `scripts/train_recognizer.py`: train / checkpoint / evaluate all models.
- `scripts/predict_topk.py`: export predicted candidate JSON for Mendis from **ordered, already isolated or annotated sign segments**.
- `tests/test_preprocessing.py`: tests preprocessing and ranking.

## 0. Installation & merging (Windows VS Code PowerShell)

1. Back up or `git status` your work first.
2. Unzip this kit *outside the repo*. Copy its `src/recognition/` and `scripts/` files **into the existing same paths**. Keep your other scripts, `dataset/`, and `.venv/` unchanged. Do not blindly replace the entire `src/recognition/` folder if you have subsequently made your own edits. The supplied files replace the earlier `TODO` architecture/train placeholders and add new scripts.
3. At the repository root, use your existing virtual environment. If TensorFlow is not installed, activate it and run:

```powershell
.\.venv\Scripts\python.exe -m pip install "tensorflow>=2.16,<2.22" "scikit-learn>=1.4" "numpy>=1.26,<3"
```

If installation fails, first check `python --version` and CPU/Windows compatibility; do **not** force-install a package for the wrong Python version. TensorFlow is configured as the default Keras backend.

## 1. Run against the already-extracted pilot NPZ files

Expected files: `dataset/processed/landmarks/pilot_hands_v1/expert_01/*.npz` and `expert_02/*.npz`.

```powershell
.\.venv\Scripts\python.exe scripts\check_landmarks.py --allow-unreviewed
```

Expected: 22 NPZ; 12 class IDs with expert_01 and 10 with expert_02. **The labels are `needs_review`; allow-unreviewed is for prototype smoke tests only.**

## 2. Train all three models on the pilot

```powershell
.\.venv\Scripts\python.exe scripts\train_recognizer.py --mode pilot --model all --epochs 5 --allow-unreviewed
```

**DO NOT claim these metrics show the best model.** Pilot mode restricts to the 10 sign IDs represented by both experts; it trains with expert_01 and checks predictions with expert_02, leaving no independent validation group. Each class has only one training video. Running repeated experiments against expert_02 and choosing settings accordingly would contaminate evaluation. Intended as a one-time pipeline **smoke test** only.

Outputs:

```text
outputs/recognition/pilot/
  labels.json
  experiment.json
  comparison.json
  lstm/model.keras, metrics.json, history.json, topk_isolated_predictions.jsonl
  gru/...
  conv1d_bilstm/...
```

Softmax outputs sum to 1 but are **not calibrated confidence estimates**. The 3 architectures do not have identical parameter counts (reported in metrics), but use the same input/splits/optimizer.

## 3. Export a sequence of Top-3 positions for Mendis (interface demonstration)

```powershell
.\.venv\Scripts\python.exe scripts\predict_topk.py --mode pilot --model gru --sequence-id DEMO001 --segments "dataset/processed/landmarks/pilot_hands_v1/expert_01/S04_go.npz" "dataset/processed/landmarks/pilot_hands_v1/expert_01/S07_school.npz"
```

The two input files are **separate isolated sign videos**, not a continuous naturally signed sequence. JSON reports `evaluation_eligible: false`. Send this only to test integration. To evaluate context accuracy, collect actual SLSL sequences with independent expert-approved boundaries and meaning ground truth; contextual metrics are NOT implemented or claimed by this package.

JSON shape:

```json
{
  "sequence_id": "DEMO001",
  "model_id": "gru",
  "score_type": "softmax_probability_uncalibrated",
  "segmentation": "provided_individual_segments_not_continuous_detection",
  "evaluation_eligible": false,
  "positions": [
    {"position": 0, "source_npz": "...", "candidates": [
      {"rank": 1, "sign_id": "S04", "gloss": "go", "score": 0.55},
      {"rank": 2, "sign_id": "S07", "gloss": "school", "score": 0.30}
    ]}
  ]
}
```

Probabilities in the JSON example are illustrative, not measured predictions.

## 4. Three-expert collection later

When v1 `.npz` data for `expert_03` are extracted into the **same NPZ root**, run:

```powershell
.\.venv\Scripts\python.exe scripts\train_recognizer.py --mode three_signer --model all --epochs 10 --allow-unreviewed
```

This mode assigns: train=expert_01, val=expert_02, test=expert_03, and retains only label IDs in **all three** experts. With one take/class, results remain very weak. For genuine signer-independent evaluation, collect several independent takes per sign and more signers; maintain a strictly untouched external test set. Remove `--allow-unreviewed` once all class labels have been confirmed and the NPZ metadata status updated. Do not edit files in-place accidentally.

**IMPORTANT:** If you collect new v1 `.npz` under `dataset/processed/landmarks/pp1_hands_v1`, change `--landmarks dataset/processed/landmarks/pp1_hands_v1`; do not point it to video `.mp4` folders. New `.mp4` must first have landmarks extracted using an updated manifest/extractor.

### Dataset and feature limits
- `pilot_hands_v1` discards second hand when two detections have the same handedness label. Pilot is preliminary. Does NOT automatically accept `pilot_hands_v2` raw slots; v2 requires correct temporal handedness tracking to create a stable two-hand feature schema.
- Initial features include wrist-relative landmark shape, absolute wrist location, and hand-detected flags. Face/body poses are not included; nonmanual cues and face-dependent distinctions cannot be learned by this baseline.
- Entire original clip is resampled, including preparation/release motion. Later apply expert-approved sign boundaries, consistently and reproducibly across models.
- Labels are visual **sign IDs**; for one sign form with Friend/Friday/February meanings, use ONE class ID and three sense IDs in Mendis's context component. The models do not guess the sense from identical hand videos.
- **Signers are never split across train/val/test.** Do not rename duplicate video copies as independent takes or train on outputs derived from test recordings.
- Save generated `outputs/recognition/` checkpoints locally; decide separately whether versioning artifacts is appropriate. Large raw videos and derived landmarks should stay ignored by Git.

## Next development phases
1. Record and verify extra expert videos; extract stable v1-style features.
2. Approved sign-boundary cropping and missing-hand diagnostics.
3. Training-only augmentations and robust independent train/validation/test signer splits.
4. Correctly annotated natural contextual sequences and Mendis's re-ranking / translation evaluation.
5. Repeated held-out-signer evaluations, macro-F1, Top-k recall and latency, plus confusion analyses.

## 5. See summary and confusion matrices

After training the models:

```powershell
.\.venv\Scripts\python.exe scripts\evaluate_recognizers.py --mode pilot
```

Look in `outputs/recognition/pilot/comparison.csv` for a small result table. Each model folder also contains `confusion_matrix.json`. The exact signer/class assignments are saved to `outputs/recognition/pilot/split_manifest.csv`.
