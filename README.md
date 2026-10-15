# Smart Sri Lankan Sign Language Recognition and Communication System

An undergraduate research project exploring Sri Lankan Sign Language (SLSL) recognition, contextual bilingual translation, learner feedback, and text/speech-to-sign communication.

**Project ID:** J26-IT-405  
**Status:** Initial development. The repository currently provides the project structure, planning documents, annotation templates, and placeholder modules. The capabilities below are planned research objectives; trained models, a working application, and measured results are not yet included.

## Project overview

The project aims to support communication between Deaf and hearing users and help learners practise SLSL. Four components share agreed sign identifiers, data formats, and integration interfaces while addressing separate research tasks.

The initial recognition prototype will classify individual sign clips captured with a phone or webcam. Contextual interpretation and evaluation will additionally use natural signed sequences. Continuous live recognition is a broader objective requiring segmentation, integration, and latency evaluation.

## Team and components

| Member      | Component | Main directory |
|---|---|---|
| Sewwandi W.M.H.    | Visual sign recognition and Top-k candidate generation | `src/recognition/` |
| Mendis W.S.K.  | Context-aware Sinhala/English interpretation and translation | `src/translation/` |
| Dewmini P.H.I. | Learner sign assessment and corrective feedback | `src/learner_feedback/` |
| Piyasiri P.D.S.V. | Text/speech-to-sign communication | `src/sign_animation/` |

### Visual sign recognition

- Extract and preprocess landmark sequences from sign videos.
- Compare LSTM, GRU, and Conv1D + BiLSTM using TensorFlow/Keras.
- Produce ranked Top-k sign candidates and identify uncertain predictions.
- Evaluate recognition accuracy, visually confusable signs, model size, and latency.
- Collaborate with the context component to compare downstream contextual accuracy.

These architectures are experimental candidates. The preferred model will be selected using validation evidence rather than assumed in advance.

### Context-aware bilingual interpretation and translation

- Use available sign context to interpret recognition candidates.
- Distinguish intended meanings where expert-validated ambiguity exists.
- Produce Sinhala and English text that preserves the intended meaning.
- Provide translated speech output through text-to-speech integration.

The current integration plan places contextual candidate selection here. The team must reconcile this boundary with the individual proposal before implementation; the outstanding ownership decision is documented in `docs/COMPONENT_OWNERSHIP.md`.

### Learner assessment and feedback

- Compare learner attempts with approved expert references.
- Assess correctness and identify errors such as handshape, location, and movement.
- Generate understandable corrective feedback.
- Evaluate on expert-reviewed learner attempts, accounting for valid sign variants.

This component can share landmark extraction utilities with recognition without depending on its trained classifier.

### Text/speech-to-sign communication

- Process text or speech input and determine its intended meaning.
- Map that meaning to an appropriate SLSL sequence and valid sign variants.
- Present sign output using approved recorded assets and/or an animation pipeline.
- Evaluate meaning preservation and output comprehensibility with SLSL expertise.

Recorded sign playback can support an initial prototype. Generated animation requires its own implementation and validation.

## Planned system workflows

| Workflow | Processing steps |
|---|---|
| Sign to text/speech | Video capture → landmark extraction → visual Top-k candidates → contextual selection → bilingual text → speech |
| Learner feedback | Learner video + intended sign → reference alignment → correctness/error assessment → feedback |
| Text/speech to sign | Text or speech → meaning/gloss processing → sign selection → recorded or animated output |

## Repository organisation

| Path | Purpose |
|---|---|
| `src/shared/` | Shared video utilities, landmark extraction, labels, and schemas |
| `src/recognition/` | Recognition architectures, training, inference, and evaluation |
| `src/translation/` | Context interpretation, bilingual translation, and speech output |
| `src/learner_feedback/` | Reference comparison, error assessment, and feedback |
| `src/sign_animation/` | Text/speech processing, sign selection, and output rendering |
| `backend/` | Planned API routes and database integration |
| `frontend/` | Planned user interface |
| `configs/` | Preprocessing, model, and evaluation settings |
| `dataset/` | Data documentation, metadata, annotations, splits, and local recordings/features |
| `models/` | Local trained models and associated inference metadata |
| `assets/` | Approved sign output assets |
| `scripts/` | Entry points for extraction, training, and evaluation |
| `tests/` | Component and integration verification |
| `results/` | Evaluation outputs and experiment records |
| `notebooks/` | Exploration and analysis |
| `docs/` | Research plans, setup guidance, ownership, and interface documentation |

See `docs/FOLDER_STRUCTURE.md` for the detailed layout.

## Technology plan

- **Recognition:** Python and TensorFlow/Keras.
- **Video and landmarks:** OpenCV and MediaPipe.
- **Analysis:** NumPy, scikit-learn, and Matplotlib.
- **Interface:** React/Vite is planned; frontend scaffolding is not yet generated.
- **Backend, translation, speech, feedback, and animation:** implementations and additional dependencies will be agreed during development.

`requirements.txt` contains proposed dependencies, not a verified version lock. Test compatibility on the agreed team environment and record exact working versions before reproducing experiments.

## Getting started

Clone the shared repository:

```bash
git clone https://github.com/ishini2003430/Smart_sign_language_recognicing_and_communication_system.git
cd Smart_sign_language_recognicing_and_communication_system
```

Create a branch for your work, for example:

```bash
git switch -c feature/recognition
```

Read `docs/SETUP.md` before configuring Python and dependencies. The application is not runnable yet; placeholder modules must be implemented first.

## Dataset approach

The team will maintain a shared, expert-reviewed vocabulary and recording index. Individual sign videos support initial visual recognition. Natural signed sequences and bilingual annotations support context and translation. Expert references and genuine learner attempts support feedback. Approved meaning-to-sign mappings and permissioned assets support sign output.

- Preserve original recordings and keep controlled backups.
- Track participant, sign, session, and source-recording identities.
- Validate similar-sign groups, meanings, and regional variants with SLSL expertise.
- Keep participant recordings, consent documents, credentials, and large model files out of ordinary Git commits.
- Document authorised dataset access separately; cloning this repository does not download the videos.
- Separate training, validation, and test data by signer where feasible, and keep derived copies together.
- State limitations explicitly when only within-signer evaluation is possible.

## Evaluation plan

Recognition experiments will compare the three visual models on the same eligible data using Top-1 accuracy, macro-F1, Top-k recall, model size, and latency. Joint evaluation will measure accuracy after the same context method, including corrected and newly introduced errors.

Translation, learner feedback, and sign output require their own task-specific evaluation and expert review. No measured performance is currently reported in this repository.

See `docs/EXPERIMENTS.md` for the proposed experimental protocol.

## Team collaboration

Develop on feature branches and use pull requests for review before merging into `main`. Members may add or reorganise internal module files. Coordinate changes to shared sign IDs, schemas, preprocessing, splits, interfaces, dependencies, and component ownership before merging.

## Documentation

- `docs/SETUP.md` — environment setup and first development milestone.
- `docs/COMPONENT_OWNERSHIP.md` — responsibilities and unresolved ownership decisions.
- `docs/RECOGNITION_TO_CONTEXT.md` — recognition/context interface proposal.
- `docs/RECORDING_PLAN.md` — recording and annotation guidance.
- `docs/EXPERT_WORD_LIST.md` — vocabulary prompts awaiting expert validation.
- `docs/EXPERIMENTS.md` — model comparison and evaluation protocol.
- `docs/SOURCES.md` — research sources and evidence limitations.

Update this README as implementation, environment verification, and evaluation progress.
