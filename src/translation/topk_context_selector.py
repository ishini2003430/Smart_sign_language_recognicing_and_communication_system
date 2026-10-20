
from .context_analyzer import load_lexicon


def get_top_candidate(position_data):
    candidates = position_data["top_k"]

    return max(
        candidates,
        key=lambda item: float(item["score"])
    )["gloss"].strip().upper()


def infer_expected_role(sequence, ambiguous_position, lexicon):
    """
    Infer a grammatical or semantic expectation from
    surrounding candidate predictions.

    These are limited prototype patterns.
    """

    glosses = [
        get_top_candidate(position)
        for position in sequence
    ]

    # Hide the ambiguous position.
    glosses[ambiguous_position] = None

    # Subject + Location + GO
    if (
        len(glosses) == 3
        and ambiguous_position == 0
        and glosses[1] in {"SCHOOL", "HOME"}
        and glosses[2] == "GO"
    ):
        return "SUBJECT"

    # Subject + GO + Location
    if (
        len(glosses) == 3
        and ambiguous_position == 0
        and glosses[1] == "GO"
        and glosses[2] in {"SCHOOL", "HOME"}
    ):
        return "SUBJECT"

    # Subject + Object + Action
    if (
        len(glosses) == 3
        and ambiguous_position == 0
        and glosses[1] in lexicon
        and glosses[2] in lexicon
    ):
        object_entry = lexicon[glosses[1]]
        action_entry = lexicon[glosses[2]]

        allowed = action_entry.get("allowed_objects", [])

        if (
            object_entry.get("grammar_role") == "OBJECT"
            and object_entry.get("concept") in allowed
        ):
            return "SUBJECT"

    # Provisional month-name context:
    # MONTH immediately before the ambiguous sign.
    if (
        ambiguous_position > 0
        and glosses[ambiguous_position - 1] == "MONTH"
    ):
        return "MONTH"

    return None


def select_candidate(sequence, ambiguous_position):
    """
    Select a Top-K candidate using contextual compatibility.

    Contextual evidence takes priority over recognition
    confidence when a supported rule is applicable.

    Otherwise, return AMBIGUOUS rather than guessing.
    """

    if not 0 <= ambiguous_position < len(sequence):
        raise ValueError("Invalid ambiguous position.")

    candidates = sequence[ambiguous_position]["top_k"]

    if not candidates:
        raise ValueError("Top-K candidates cannot be empty.")

    lexicon = load_lexicon()

    expected_role = infer_expected_role(
        sequence,
        ambiguous_position,
        lexicon
    )

    ranked = []

    for item in candidates:
        gloss = item["gloss"].strip().upper()
        recognition_score = float(item["score"])

        entry = lexicon.get(gloss, {})

        grammar_role = entry.get("grammar_role")
        semantic_type = entry.get("semantic_type")

        context_score = 0
        reasons = []

        if expected_role == "SUBJECT":
            if grammar_role == "SUBJECT":
                context_score = 2
                reasons.append(
                    "Candidate fits the expected subject role."
                )
            elif grammar_role in {
                "OBJECT_PRONOUN",
                "POSSESSIVE_PRONOUN"
            }:
                context_score = -2
                reasons.append(
                    "Candidate conflicts with the expected "
                    "English subject role."
                )

        elif expected_role == "MONTH":
            if semantic_type == "MONTH":
                context_score = 2
                reasons.append(
                    "Candidate is a month name and matches "
                    "the provisional MONTH contextual cue."
                )

        ranked.append({
            "gloss": gloss,
            "recognition_score": recognition_score,
            "context_score": context_score,
            "reasons": reasons
        })

    ranked.sort(
        key=lambda item: (
            item["context_score"],
            item["recognition_score"]
        ),
        reverse=True
    )

    baseline = max(
        ranked,
        key=lambda item: item["recognition_score"]
    )["gloss"]

    best = ranked[0]

    # A clear positive contextual rule must be available.
    winners = [
        item for item in ranked
        if item["context_score"] == best["context_score"]
    ]

    if best["context_score"] <= 0 or len(winners) != 1:
        return {
            "status": "AMBIGUOUS",
            "selected": None,
            "recognition_baseline": baseline,
            "ranked_candidates": ranked,
            "expected_role": expected_role,
            "reason": "Insufficient or non-unique context evidence."
        }

    return {
        "status": "RESOLVED",
        "selected": best["gloss"],
        "recognition_baseline": baseline,
        "ranked_candidates": ranked,
        "expected_role": expected_role,
        "reason": (
            "Selected using contextual grammatical "
            "or semantic compatibility."
        )
    }
