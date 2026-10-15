# Smart SLSL: reviewed TensorFlow/Keras starter
Prepared 13 October 2026. Recording visit: 14 October 2026.

STATUS: folder skeleton, planning documents and annotation templates only. No working model, application, trained weights, measured accuracy or verified dependency lock is supplied. Python files contain role descriptions only.

Framework: TensorFlow/Keras for Sewwandi's recognition experiments. Three planned visual models: LSTM, GRU, Conv1D + BiLSTM. These are justified candidates, not proven best models.

## Read first
1. docs/RECORDING_PLAN.md and docs/EXPERT_WORD_LIST.md before recording.
2. docs/COMPONENT_OWNERSHIP.md: panel notice conflicts with individual report about context ownership.
3. docs/RECOGNITION_TO_CONTEXT.md: proposed versioned interface for team review.
4. docs/EXPERIMENTS.md: fair comparison, signer splits and evaluation.
5. docs/SETUP.md: environment and repository use.

The panel-aligned default places recognition, Top-k and uncertainty under Sewwandi; candidate meaning selection, translation and translated-output TTS under Sahan/Mendis. The individual report assigns contextual re-ranking to Sewwandi. Record the supervisor/team decision and align the report and ownership document. Do not develop two independent re-rankers accidentally.

The four components have separate flows. Learner feedback does not require the trained recognizer. Text/speech-to-sign does not depend on the recognition output. Shared extraction utilities can serve both recognition and feedback with task-specific preprocessing.

## Repository installation
Extract this ZIP and copy the CONTENTS of smart_slsl_tensorflow_pp1 into a clone of the existing team repository. Preserve its .git directory. Merge existing README/config files; do not blindly overwrite teammates' work. Use a branch and pull request. No new git init is needed inside a clone.

Everyone may add, remove or reorganize internal files. Coordinate shared IDs, data splits, schemas, APIs, dependency changes and ownership first. Keep raw recordings immutable. Generated features and model outputs may be rebuilt; raw data and annotations need backed-up version history outside ordinary Git.

See docs/FOLDER_STRUCTURE.md for the complete generated tree. Files in models/ will hold trained .keras models plus class maps, preprocessing definitions and package versions; src/recognition/architectures/ holds Python model-building code.
