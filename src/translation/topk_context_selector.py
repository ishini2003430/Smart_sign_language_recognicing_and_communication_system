
def select_candidate(sequence, ambiguous_position):
    """
    Select a Top-K candidate based on contextual compatibility.

    Prototype rule:
    In the pattern PRONOUN + GO + SCHOOL,
    the English subject form I is preferred over ME.

    Recognition confidence is used to rank the input,
    but strong grammatical context can override it.
    """

    if not 0 <= ambiguous_position < len(sequence):
        raise ValueError("Invalid ambiguous position.")

    candidates = sequence[ambiguous_position]["top_k"]

    if not candidates:
        raise ValueError("Top-K candidates cannot be empty.")

    # Normalize candidate words and preserve their scores.
    normalized = [
        {
            "gloss": item["gloss"].strip().upper(),
            "recognition_score": float(item["score"]),
            "context_score": 0,
            "reasons": []
        }
        for item in candidates
    ]

    # Use the highest-scoring candidate at other positions
    # as provisional surrounding context.
    surrounding = []

    for index, position_data in enumerate(sequence):
        if index == ambiguous_position:
            surrounding.append(None)
            continue

        top_candidate = max(
            position_data["top_k"],
            key=lambda item: float(item["score"])
        )
        surrounding.append(
            top_candidate["gloss"].strip().upper()
        )

    # Explicit prototype context pattern.
    has_subject_context = (
        ambiguous_position == 0
        and len(surrounding) == 3
        and surrounding[1:] == ["GO", "SCHOOL"]
    )

    for candidate in normalized:
        if has_subject_context:
            if candidate["gloss"] == "I":
                candidate["context_score"] = 1
                candidate["reasons"].append(
                    "I is the English subject form "
                    "for the GO + SCHOOL sentence pattern."
                )
            elif candidate["gloss"] == "ME":
                candidate["context_score"] = -1
                candidate["reasons"].append(
                    "ME is not the standard English subject form."
                )

    # Rank by contextual compatibility first,
    # then recognition confidence as a tie-breaker.
    ranked = sorted(
        normalized,
        key=lambda item: (
            item["context_score"],
            item["recognition_score"]
        ),
        reverse=True
    )

    winner = ranked[0]

    if len(ranked) > 1 and (
        winner["context_score"] == ranked[1]["context_score"]
    ):
        return {
            "status": "AMBIGUOUS",
            "selected": None,
            "recognition_baseline": max(
                normalized,
                key=lambda item: item["recognition_score"]
            )["gloss"],
            "ranked_candidates": ranked,
            "reason": "Context did not distinguish the candidates."
        }

    return {
        "status": "RESOLVED",
        "selected": winner["gloss"],
        "recognition_baseline": max(
            normalized,
            key=lambda item: item["recognition_score"]
        )["gloss"],
        "ranked_candidates": ranked,
        "reason": "Selected using contextual compatibility."
    }
