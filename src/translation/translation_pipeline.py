
from .app import translate_signs
from .topk_context_selector import select_candidate


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


def translate_topk_sequence(sequence):
    """
    Resolve simulated Top-K recognition predictions and
    generate English and Sinhala sentences.
    """

    if not sequence:
        raise ValueError("Input sequence cannot be empty.")

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
