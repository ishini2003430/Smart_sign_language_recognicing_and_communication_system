# PP1 evidence checklist — proposed, not an official marking rubric

Confirm the panel/supervisor milestones; this checklist cannot guarantee a pass.
- Record one agreed owner of contextual candidate re-ranking. The panel handoff and individual report currently differ.
- Expert-approved vocabulary, confusable contrasts, consent references, participant counts and dataset limitations.
- Demonstrate original phone video -> inspected landmarks -> saved features -> visual candidate output.
- Compare LSTM, GRU and Conv1D+BiLSTM with identical eligible data and comparable tuning budgets.
- Show Top-1, macro-F1, Top-k recall and the SAME context selector's downstream accuracy for each model.
- Include recovery and harm, class/signer breakdowns, latency including window capture, and examples of failure.
- Keep sign-form accuracy separate from meaning/sense accuracy. State if only within-signer or manual-boundary evaluation is available.
- Show each teammate's own implemented flow and the shared interface. A folder skeleton is not implementation progress.
- Report what is actually completed; do not present staged output or tiny-batch overfitting as evaluation.

The exact named SLSL confusable pairs and polysemous forms remain pending expert validation. Ask about both because the panel wording mentions similar gestures with multiple meanings, while the report distinguishes visual ambiguity from sense ambiguity.
