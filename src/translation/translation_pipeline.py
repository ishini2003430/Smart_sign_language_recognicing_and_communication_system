
from .app import translate_signs
from .topk_context_selector import select_candidate
from itertools import product


def prepare_for_grammar(glosses):
    """
    Convert explicitly supported input orders into the order
    expected by the existing sentence reconstruction engine.

    These are prototype conventions, not validated SLSL grammar.
    """
    if (
        len(glosses) == 3
        and glosses[0] in {"I", "YOU"}
        and glosses[1] == "GO"
        and glosses[2] in {"SCHOOL", "HOME"}
    ):
        return [glosses[0], glosses[2], glosses[1]]

    return glosses

    
def evaluate_full_sequences(sequence):
    """
    Evaluate combinations of Top-K candidates using the
    existing bilingual grammar engine.

    Select a sequence only when exactly one distinct
    sequence matches a supported grammar pattern.
    """

    candidate_lists = []

    for position in sequence:
        candidates = position["top_k"]

        candidate_lists.append([
            {
                "gloss": item["gloss"].strip().upper(),
                "score": float(item["score"])
            }
            for item in candidates
        ])

    total_combinations = 1

    for candidates in candidate_lists:
        total_combinations *= len(candidates)

    if total_combinations > 500:
        return {
            "status": "AMBIGUOUS",
            "selected_glosses": None,
            "decisions": [],
            "english": None,
            "sinhala": None,
            "pattern": None,
            "reason": (
                "Too many candidate combinations to "
                "evaluate in this prototype."
            )
        }

    valid_sequences = {}

    for combination in product(*candidate_lists):
        glosses = [item["gloss"] for item in combination]

        grammar_glosses = prepare_for_grammar(glosses)
        translation = translate_signs(grammar_glosses)

        if translation["pattern"] == "UNKNOWN":
            continue

        key = tuple(glosses)

        valid_sequences[key] = {
            "selected_glosses": glosses,
            "grammar_glosses": grammar_glosses,
            "translation": translation,
        }

    if len(valid_sequences) == 0:
        return {
            "status": "UNSUPPORTED_PATTERN",
            "selected_glosses": None,
            "decisions": [],
            "english": None,
            "sinhala": None,
            "pattern": "UNKNOWN",
            "reason": (
                "No candidate combination matched "
                "a supported grammar pattern."
            )
        }

    if len(valid_sequences) > 1:
        return {
            "status": "AMBIGUOUS",
            "selected_glosses": None,
            "decisions": [],
            "english": None,
            "sinhala": None,
            "pattern": None,
            "possible_sequences": [
                list(glosses)
                for glosses in valid_sequences
            ],
            "reason": (
                "Multiple candidate sequences are "
                "grammatically possible. More context "
                "is required to determine the meaning."
            )
        }

    winner = next(iter(valid_sequences.values()))

    decisions = []

    for index, chosen_gloss in enumerate(
        winner["selected_glosses"]
    ):
        candidates = candidate_lists[index]

        baseline = max(
            candidates,
            key=lambda item: item["score"]
        )["gloss"]

        decisions.append({
            "position": index,
            "status": (
                "RESOLVED"
                if len(candidates) > 1
                else "SINGLE_CANDIDATE"
            ),
            "selected": chosen_gloss,
            "recognition_baseline": baseline,
            "reason": (
                "The selected candidate belongs to the "
                "only sequence supported by the current "
                "grammar engine."
            )
        })

    translation = winner["translation"]

    return {
        "status": "SUCCESS",
        "selected_glosses": winner["selected_glosses"],
        "grammar_glosses": winner["grammar_glosses"],
        "decisions": decisions,
        "english": translation["english"],
        "sinhala": translation["sinhala"],
        "pattern": translation["pattern"],
        "reason": (
            "Selected the unique grammatically "
            "supported candidate sequence."
        )
    }



def translate_topk_sequence(sequence):
    """
    Resolve simulated Top-K recognition predictions and
    generate English and Sinhala sentences.
    """

    if not sequence:
        raise ValueError("Input sequence cannot be empty.")

        # Count sign positions with multiple candidates.
    ambiguous_positions = sum(
        1
        for position in sequence
        if len(position["top_k"]) > 1
    )

    # If multiple positions are ambiguous,
    # evaluate complete candidate sequences.
    if ambiguous_positions > 1:
        return evaluate_full_sequences(sequence)


    selected_glosses = []
    decisions = []

    for position, sign_data in enumerate(sequence):
        candidates = sign_data.get("top_k", [])

        if not candidates:
            raise ValueError(
                f"Missing Top-K candidates at position {position}."
            )

        if len(candidates) == 1:
            selected = candidates[0]["gloss"].strip().upper()

            decisions.append({
                "position": position,
                "status": "SINGLE_CANDIDATE",
                "selected": selected,
                "recognition_baseline": selected,
                "reason": "Only one candidate was provided."
            })

        else:
            result = select_candidate(sequence, position)

            decisions.append({
                "position": position,
                **result
            })

            if result["status"] != "RESOLVED":
                return {
                    "status": "AMBIGUOUS",
                    "selected_glosses": None,
                    "decisions": decisions,
                    "english": None,
                    "sinhala": None,
                    "pattern": None,
                    "reason": (
                        "At least one sign could not be "
                        "resolved using the available context."
                    )
                }

            selected = result["selected"]

        selected_glosses.append(selected)

    grammar_glosses = prepare_for_grammar(selected_glosses)

    translation = translate_signs(grammar_glosses)

    if translation["pattern"] == "UNKNOWN":
        return {
            "status": "UNSUPPORTED_PATTERN",
            "selected_glosses": selected_glosses,
            "decisions": decisions,
            "english": None,
            "sinhala": None,
            "pattern": "UNKNOWN",
            "reason": (
                "Candidates were selected, but the existing "
                "grammar engine does not support this sequence."
            )
        }

    return {
        "status": "SUCCESS",
        "selected_glosses": selected_glosses,
        "grammar_glosses": grammar_glosses,
        "decisions": decisions,
        "english": translation["english"],
        "sinhala": translation["sinhala"],
        "pattern": translation["pattern"]
    }
