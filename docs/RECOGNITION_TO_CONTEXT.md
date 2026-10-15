# Proposed API contract v0.1
Panel-aligned handoff; review together before implementing.
Recognition produces window ID, timestamps, model ID, vocabulary version, Top-k form candidates, scores, uncertainty and feature-quality flags. Previous context must contain only information available at inference time, ordinarily previous recognized forms/senses. Do not send the hidden target label from annotations.
Context selection returns selected candidate form ID, sense ID where available, resolution status and method version. If unresolved, return unresolved/abstain; a language model must not invent an unsupported certainty.

The fixture uses synthetic FORM_A/FORM_B IDs and fabricated scores for integration only; these are not real SLSL words or evidence. Candidate scores cover only the reported Top-k and need not sum to 1. For true same-form multiple meanings, expand via sign_senses.json; do not divide the form score arbitrarily and call it a learned sense probability.

Meaning, gloss and bilingual text are different fields. Piyasiri uses the meaning-to-output-sign mapping in the reverse direction. Version the registry, feature schema and API together when changing labels. Log both initial and final predictions for the same window/recording ID so recovery/harm can be audited.
