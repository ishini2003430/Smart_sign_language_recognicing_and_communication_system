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
