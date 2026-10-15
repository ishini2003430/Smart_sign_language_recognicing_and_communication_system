# Recognition experiments
## The three planned visual models
1. LSTM: temporal recurrent baseline.
2. GRU: alternative gated recurrent baseline for accuracy/latency comparison.
3. Conv1D + BiLSTM: short temporal patterns followed by bidirectional modelling of a completed sign window.

These can all be built in TensorFlow/Keras. The hybrid is motivated by SLSL work using MaskedConv1D + BiLSTM + attention, but a plain Conv1D + BiLSTM implementation is an adaptation, not an exact reproduction. No evidence establishes these as the best three on the uncollected dataset. Freeze this manageable comparison rather than adding models without a research reason.

Example starting sizes, subject to validation: LSTM(64); GRU(64); Conv1D(32,kernel=3) followed by Bidirectional(LSTM(32)). Each ends with Dropout(0.3), Dense(32,relu), Dense(C,softmax). C is the approved number of visual form classes. Same unit count does not mean equal parameter count; report parameters, training time and memory. Match the tuning budget and preprocessing, not just model names.

## Inputs and scope
Use complete sign-window landmark sequences, both hands and body-relative pose; preserve face/mouth features when required by the expert's contrasts. Inspect extraction quality first. Keep raw features, timestamps, handedness, missingness and detection confidence. MediaPipe confidence is not sign-class confidence. Predicted depth is not calibrated sensor depth.
Choose a common fixed-length temporal resampling policy after inspecting duration/speed (48 frames is only a candidate). All models use the same feature order, normalization and duration information. Do not fill absent-hand tracks as invented observed motion. If variable-length padding is used, implement/test masks through every model; ordinary Conv1D does not automatically implement the cited paper's MaskedConv1D behavior.

A BiLSTM uses future frames within its window. All three can classify completed sign segments, but none of these classifier files alone solves continuous segmentation. Prototype manual/record-button boundaries first; report that scope. Continuous signing needs boundary detection/training, transitions, natural sequence evaluation and optionally a sequence-alignment model later. Include capture/window waiting, extraction, recognition, context and rendering in end-to-end latency. Do not describe a model-only millisecond timing as full real-time performance.

## Labels for ambiguity
Different forms with similar appearance have different classes. One indistinguishable visual form with multiple meanings has one form class plus several sense IDs. Sahan expands candidate forms into compatible senses and uses context. Evaluate form accuracy separately from intended meaning accuracy. Scores produced by softmax are not automatically calibrated probabilities of correctness.

## Fair protocol
Use the same signer-disjoint train/validation/test manifests, vocabulary, input features, augmentation rules, seeds and stopping/tuning budget for all 3 models. Train only on the training split. Use validation for hyperparameters, thresholds, Top-k (e.g. 1/3/5 if C permits) and score calibration. Keep the context method and its training corpus fixed across visual models; tune comparable per-model settings on validation only. Include repeat seeds if feasible and report per-signer results and uncertainty in estimates.
For each visual model compare:
A. Direct visual Top-1 form decision.
B. The same model with Top-k + the SAME context selector.
C. Optionally an always-context baseline versus uncertainty-gated context.
For sense evaluation, define an explicit context-free default-sense baseline learned from training data when a form has multiple senses. Do not conflate this with form classification accuracy.

Metrics: Top-1 form accuracy, macro-F1, Top-k form recall; intended sense accuracy after context; confusable-group scores; recovery and harm counts/rates; latency and model size. Report the denominator for each rate. Recovery rate = baseline-wrong cases corrected / all baseline-wrong cases. Harm rate = baseline-correct cases made wrong / all baseline-correct cases. Candidate-constrained context cannot recover a correct form absent from Top-k; report that upper bound separately. Abstentions/rejections must be reported with coverage, not excluded to inflate accuracy.
Keep the input video and recognized preceding context identical between relevant comparisons. Ground-truth context is an oracle diagnostic only, never the headline deployed score. Do not let templates or copied target labels leak into the predictor.
Select the preferred model on validation post-context accuracy with an agreed latency constraint and tie-break rule (e.g. macro-F1 then latency); lock it before final testing. Present test comparisons as evaluation, not repeated tuning. Novelty must be argued from experiments and prior work, not from using a framework or stacking existing layers.
