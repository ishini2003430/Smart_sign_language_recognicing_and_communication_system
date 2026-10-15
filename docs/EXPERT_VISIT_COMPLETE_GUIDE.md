# Expert consultation and draft vocabulary
Visit: 14 October 2026. This is an elicitation list, NOT a verified SLSL dictionary or a list of confirmed minimal pairs.

## Explain the project to the expert
We are building (1) sign recognition with several candidate outputs for difficult signs, (2) context-based Sinhala/English interpretation, (3) feedback on learner handshape/location/movement errors, and (4) text/speech-to-sign output. Please help select a small coherent vocabulary, validate natural signs and sentences, and identify real visual ambiguities.

## Twenty everyday concepts to review
English and Sinhala here identify intended concepts; the expert supplies the actual SLSL form, appropriate gloss, regional variant, and natural sentence use. A written word is not automatically one sign. Do not force one-to-one spoken-language word order.

| Draft ID | English concept | Sinhala prompt |
|---|---|---|
| D01 | I / me | මම / මට |
| D02 | you | ඔබ / ඔයා |
| D03 | mother | අම්මා |
| D04 | father | තාත්තා |
| D05 | child | දරුවා |
| D06 | doctor | වෛද්‍යවරයා |
| D07 | hospital | රෝහල |
| D08 | home | ගෙදර |
| D09 | school | පාසල |
| D10 | water | වතුර |
| D11 | food | ආහාර |
| D12 | medicine | බෙහෙත් |
| D13 | eat | කන්න |
| D14 | drink | බොන්න |
| D15 | go | යන්න |
| D16 | come | එන්න |
| D17 | want / need (expert distinguishes) | අවශ්‍යයි / ඕනෑ |
| D18 | pain / hurt (expert distinguishes) | වේදනාව / රිදෙනවා |
| D19 | today | අද |
| D20 | tomorrow | හෙට |

## Ten reserved positions: the research-critical signs
Ask for FIVE pairs of distinct signs that look similar but mean different things. Fill slots D21-D30 with these ten sign forms. Prefer common signs that can appear in natural short contexts using the core vocabulary. If a chosen form is already in D01-D20, reuse its form ID and fill the spare slot with another useful context sign. Final class count follows validated distinct forms, not the number of words printed here.

For each pair record: both meanings, approved glosses, exact difference (handshape, orientation, location, movement, or non-manual feature), regional scope, and 3 different natural contexts per target sign. Use the term minimal pair only when the expert confirms a single contrastive parameter. Otherwise label visually confusable pair/group. If no suitable pair is confirmed, leave it pending rather than inventing one.

Separately ask whether 3-5 sign forms have multiple meanings that genuinely require context. This is an exploration target, not a claim these forms exist in this vocabulary. Record each meaning and at least 3 natural contexts per meaning. Check whether facial expression, mouth action, body position or movement already distinguishes the forms; apparent hand similarity alone is not identity.

Do NOT assume English examples such as bank, right or light share a single SLSL sign. Do NOT assume related words such as mother/father are a minimal pair.

## Distinguish three situations
1. Different forms, similar appearance: separate form IDs, separate recognition classes, shared confusion-group ID.
2. Same observable form, different meanings: one form ID and multiple sense IDs. Recognition ranks forms; context selects the sense. Never give the exact same isolated gesture two contradictory visual labels and expect the classifier to infer invisible context.
3. Same meaning, different valid regional forms: variant IDs/notes. Do not label valid dialect variation as learner error.

## Meaning prompts for natural sentences
These are elicitation prompts, NOT asserted SLSL gloss sequences:
- I want water.
- The child drinks water.
- Mother wants medicine.
- Father goes to the hospital today.
- I go to school tomorrow.
- The child wants food.
- I want to go home.
- I need a doctor.
Have the expert reformulate naturally, identify required signs and annotate actual gloss order. Replace prompts or extend the vocabulary if necessary. Record full signing, not edited concatenations of isolated dictionary clips.

## Before approving each entry
Confirm form ID, gloss, Sinhala and English sense, handedness/variant, required face/body features, visual contrast, example contexts, reference clip, reviewer ID and review date. Draft IDs are not permanent class labels. Final approved entries go in sign_registry.json and sign_senses.json.


---

# Recording plan for 14 October 2026
Planning recommendation, not a universal sample-size rule or guarantee of accuracy.

## Phone setup
A normal RGB phone camera is a reasonable collection tool. Start with the rear camera, normal video, landscape 1080p at 30 fps, stable tripod/support and even front lighting. Use 60 fps only if a pilot shows fast finger motion is blurred/missed and the lighting/storage allow it. More frames do not fix poor exposure. Avoid portrait/cinematic blur, filters, digital zoom and intentionally slowed signing.
Frame the head, face, torso, elbows and the entire reach of both hands. Distance is determined by signing space and readable fingers, not a fixed number of metres. Ask the signer to perform the widest sign before setting the frame. A plain background and contrasting plain clothing help. Record facial expression and mouth actions naturally. Do not crop to hands alone.
Keep original files, resolution, actual frame timestamps and frame rate. Use file transfer or original-quality upload, not compressed chat-video copies. Log any mirroring, rotation and camera changes. Retain originals before any conversion. Camera timestamps matter if the phone records variable frame rate.

## Pilot first: 10-15 clips
Record one-handed, two-handed, fast, face-adjacent and expert-selected confusing signs. Copy files to a laptop. Inspect finger clarity, full motion, video decoding and hand/pose tracking if available. If extraction is not ready, at least inspect every pilot visually; do not claim tracking was tested. Adjust framing/light before the main recording. Both hands must be enabled in the extractor. Record a small webcam subset later if the demo uses a webcam; phone quality does not establish webcam robustness.

## Participants
One qualified SLSL expert can validate vocabulary and supervise. The recognition dataset needs several fluent SLSL signers, not necessarily several certified instructors. Aim for 5 fluent signers for a small initial experiment; more varied signers later improve the evidence. Include proficient Deaf SLSL users where possible and document regional variants. A second independent qualified reviewer is useful for uncertain pairs and error labels.
One person repeated many times cannot establish signer independence. Beginners belong in the learner dataset; incorrect learner signs must not be silently added as correct recognition examples.
Use the institution's participant-consent process, explaining research recording, access, demonstration/publication and any public video playback separately. Store personal consent and the ID key securely outside Git. Anonymous filenames do not make visible faces anonymous. Participation should be voluntary and allow breaks.

## Recording quantities
| Collection | Planning target | Use |
|---|---|---|
| Isolated signs, full pilot dataset | 30 approved forms x 5 fluent signers x 10 fresh takes = 1,500 clips | Shared visual training/evaluation |
| Tomorrow, if only one signer | 30 x 1 x 5 = 150 clips | Extraction/model pilot only; collect other signers later |
| Tomorrow, if three signers | 30 x 3 x 5 = 450 clips | Useful first session, still limited generalization evidence |
| Context for 5 distinct-form pairs | 5 pairs x 2 targets x 3 context templates x 5 signers x 2 takes = 300 full utterances | Context training and evaluation |
| Optional true multi-meaning set | Example: 3 forms x 2 senses x 3 contexts x 5 signers x 2 takes = 180 utterances | Only if expert confirms these cases |
| Clean reference/output takes | 30 forms x 2 clean takes = 60 | Expert reference and permitted output assets; eligible existing takes may be reused |
| Natural learner pilot | 10 signs x 5 learners x 3 attempts = 150 | Correctness/error feedback; labels are assigned after review |
| Background/no-sign pilot | 5 signers x 10 short clips = 50 | Idle, transitions and ordinary non-sign movement for rejection/segmentation |

These are targets for a small study, not a claim all can be recorded tomorrow. Context templates may need additional approved signs. Recompute counts from the final registry. A 1,500-clip count is NOT 1,500 independent participants. Do not count duplicated files, resampled frames or augmentation as fresh recordings. Reused reference clips retain one source recording ID and one split.

## How to record isolated signs
One take contains one complete sign at natural speed, with about 0.5-1 second neutral space before and after. Do not cut a long sign short to meet a duration. Freshly perform each repetition. Collect in rounds rather than 10 rapid robotic repeats; use breaks. If practical, spread takes across two sessions. Keep natural variation without changing meaning. Never deliberately perform an incorrect sign in the correct-sign training set.
Assign a recording ID immediately. Example: S03_F021_SE02_T04.mp4 = signer 3, form 21, session 2, take 4. No personal name in the filename. Log speaker-independent IDs for context and learner recordings too.
If using a continuous recording containing many takes, keep the original and annotate all take boundaries; every child clip retains that parent recording ID.

## Context: essential, not optional for the context claim
An isolated-word dataset cannot demonstrate contextual recovery. Record complete natural signed utterances and, where needed, preceding discourse. For every difficult target, collect several contexts per meaning with expert gloss order and Sinhala/English translations. Do not whisper/say the target label in model input or let answer cards enter the frame.
Capture the target's form ID, intended sense ID, onset/offset and actual available context. Preserve non-manual cues. Keep contexts varied and balanced across meanings; avoid every target being uniquely identified by a single fixed sentence. If a meaning genuinely remains ambiguous, mark it unresolved; do not force a fabricated ground truth.
Main online experiment uses preceding recognized context only. Future context experiments are separate and must include waiting latency. Gold gloss context may be used only in an explicitly labelled oracle diagnostic.

## Data for Dewmini and Piyasiri
Dewmini needs correct expert reference takes AND genuine learner attempts reviewed for correctness, handshape, location, movement, multiple errors, uncertainty and valid variants. Ten selected teaching signs are a manageable start. Expert demonstrations of 1 controlled error per category per sign (10 x 3 = 30 staged error clips, plus correct references) can explain the task, but must be marked staged and cannot replace evaluation on genuine learners. Natural attempts will not necessarily yield balanced error categories; collect more if needed. Keep learner IDs split-disjoint.
Piyasiri needs approved text/meaning-to-sign mappings, context-sensitive variants, natural reference sequences and clean output assets with appropriate permission. Reuse eligible references through manifests rather than copying data into splits. If 3D animation is required, separately design/validate avatar motion and transitions; RGB video collection does not by itself implement or validate animation.

## Annotations and quality checks
Recording manifest: recording ID, parent recording ID, relative path, signer ID, session, take, type, device ID, fps, frame size, duration, lighting, background, angle, mirroring, review status and consent-reference ID.
Sign registry: stable form ID, gloss and variant. Sense mapping: form ID to sense IDs and bilingual meanings. Confusable groups: members and expert-validated differences. Sequence labels: actual gloss/form order, sense IDs, sign time boundaries, translations and context-template ID. Learner labels: intended form, observed error tags, expert notes and reviewer.
Reject/re-record clips with cropped hands, unreadable motion, wrong execution or uncertain labels as appropriate. Keep rejected clips out of training using status flags, not silent relabelling. Track failures by sign and signer so difficult signs are not disproportionately removed.

## Splits and leakage
Split by signer before deriving training samples. With 5 fluent signers, an illustrative initial split is 3 training / 1 validation / 1 test. All forms need coverage in each split. One held-out test signer is preliminary evidence only; rotate held-out signers with nested tuning or collect more for stronger evaluation. With one signer, only a within-signer pilot is possible.
Never randomly split neighbouring frames, takes cut from the same recording or augmented copies across splits. Keep all uses of a source clip together. Do not let a held-out signer's expert reference/output video enter model development. Separate public output assets from evaluation inputs by provenance.
For context generalization, ALSO hold out sentence/context template IDs: reserve one template per target for validation and another for test, and do not train on those templates recorded by training signers. This stricter intersection reduces usable examples, so collect additional training templates as time allows. Preserve all raw recordings but select eligible subsets with explicit manifests. A signer-only split with seen sentences measures a narrower task and must be named accordingly. Keep all three models on the same eligible samples.
Fit normalization and train augmentation on training data only. No automatic horizontal flipping unless the expert confirms label preservation. Do not normalize each hand independently in a way that erases body-relative location or orientation needed by a contrast.

## Tomorrow's order
1. Review vocabulary, difficult pairs and meaning cases with the expert; assign stable approved IDs.
2. Confirm consent, framing and a 10-15-clip pilot; inspect before proceeding.
3. Capture isolated signs in rounds, prioritizing difficult pairs and all participating signers.
4. Capture full context sentences while expert access is available.
5. Select clean reference takes and record learner-error guidance; schedule genuine learners if unavailable.
6. Review counts and labels together; copy originals to two controlled locations and reopen samples from the backup.
7. Record what remains missing and arrange the additional signers/sessions. Reduce vocabulary before sacrificing reliable labels, context or participant variety.
