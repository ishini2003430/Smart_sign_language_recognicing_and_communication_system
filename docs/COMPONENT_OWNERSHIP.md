# Component boundaries and evidence
Reviewed: team topic assessment form TAF-J26-IT-405.pdf (especially pp. 7-9); IT23205710 (1).pdf (especially pp. 23-26); panel notice image.png. Other members' individual reports and Dewmini's original full folder tree were not available for a fresh audit. This is a proposal covering the documented tasks, not certification of unseen requirements.

| Owner | Directory | Responsibility |
|---|---|---|
| Sewwandi | src/recognition | Landmark-sequence classifiers, 3-model training, uncertainty, Top-k, latency and confusion analysis |
| Sahan / Mendis W.S.K | src/translation | Context candidate/meaning selection, bilingual grammar and translation, translated-output TTS |
| Dewmini | src/learner_feedback | Expert references, learner alignment, correctness, error categories, Sinhala/English feedback, learner evaluation |
| Piyasiri | src/sign_animation | Text/speech processing, gloss generation, context-sensitive output-sign selection, recorded-video or animation rendering |
| Team | src/shared, dataset, backend, frontend, tests | IDs, utilities, collection, interfaces and integration |

## Decision that must be recorded
Panel notice: Sewwandi trains 3 models and supplies Top-k to component 4; contextual accuracy informs model justification. Sahan/Mendis determines meaning from context.
Individual report: contextual candidate re-ranking is assigned to Sewwandi.
This skeleton follows the explicit panel handoff. Supervisor/team should confirm this and update the inconsistent individual responsibility table. If ownership is changed, move the context package and update imports/contracts, without creating a second implementation. Sewwandi and Sahan jointly evaluate the complete recognition/context pipeline.

Sahan's selection interprets incoming sign candidates. Piyasiri's selection chooses outgoing signs given input meaning. These are different tasks. TTS for translated output has a default owner of Sahan based on the detailed team task list; accessibility controls may be shared.

## Changes teammates can make
Internal helper files and subfolders: yes, in their branches. Shared sign IDs, sense mappings, API response shapes, preprocessing definition, split assignments, environment constraints and module boundaries: agree and version first. Do not silently rename IDs or change test data after inspecting results.
Recorded sign playback is a useful prototype for output, but is not a completed 3D animation system. Keep an explicit animation renderer and evaluation task if the approved component requires generated animation.
