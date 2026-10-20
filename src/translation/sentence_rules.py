
def unknown_result():
    return {
        "english": None,
        "sinhala": None,
        "pattern": "UNKNOWN"
    }


def reconstruct_sentence(signs, lexicon):
    """
    Reconstruct bilingual sentences using supported
    grammatical and semantic patterns.

    Input word orders are provisional prototype conventions.
    """

    signs = [sign.strip().upper() for sign in signs]

    if len(signs) != 3:
        return unknown_result()

    if any(sign not in lexicon for sign in signs):
        return unknown_result()

    # The first gloss must represent a subject.
    subject_gloss = signs[0]
    subject = lexicon[subject_gloss]

    if subject.get("grammar_role") != "SUBJECT":
        return unknown_result()

    if subject_gloss not in {"I", "YOU"}:
        return unknown_result()

    # Recognize supported word orders:
    # SUBJECT + OBJECT/LOCATION + ACTION
    # SUBJECT + ACTION + OBJECT/LOCATION

    second = lexicon[signs[1]]
    third = lexicon[signs[2]]

    if second.get("grammar_role") == "ACTION":
        action_gloss = signs[1]
        middle_gloss = signs[2]
    elif third.get("grammar_role") == "ACTION":
        action_gloss = signs[2]
        middle_gloss = signs[1]
    else:
        return unknown_result()

    action = lexicon[action_gloss]
    middle = lexicon[middle_gloss]
    middle_role = middle.get("grammar_role")

    english_subject = "I" if subject_gloss == "I" else "You"
    sinhala_subject = subject["sinhala"]

    # Pattern 1: Subject + Location + GO / COME

    if middle_role == "LOCATION" and action_gloss in {
        "GO", "COME"
    }:
        if middle_gloss == "SCHOOL":
            english_location = "to school"
            sinhala_location = "පාසලට"
        elif middle_gloss == "HOME":
            english_location = "home"
            sinhala_location = "ගෙදර"
        else:
            return unknown_result()

        if action_gloss == "GO":
            english_verb = (
                "am going" if subject_gloss == "I"
                else "are going"
            )
            sinhala_verb = "යනවා"
        else:
            english_verb = (
                "am coming" if subject_gloss == "I"
                else "are coming"
            )
            sinhala_verb = "එනවා"

        return {
            "english": (
                f"{english_subject} {english_verb} "
                f"{english_location}."
            ),
            "sinhala": (
                f"{sinhala_subject} "
                f"{sinhala_location} {sinhala_verb}."
            ),
            "pattern": "SUBJECT_LOCATION_ACTION"
        }

    # Pattern 2: Subject + Object + EAT / DRINK

    if middle_role == "OBJECT" and action_gloss in {
        "EAT", "DRINK"
    }:
        allowed_objects = action.get("allowed_objects", [])

        if middle.get("concept") not in allowed_objects:
            return unknown_result()

        english_verb = action["english"]
        english_object = middle["english"]

        return {
            "english": (
                f"{english_subject} "
                f"{english_verb} {english_object}."
            ),
            "sinhala": (
                f"{sinhala_subject} "
                f"{middle['sinhala']} {action['sinhala']}."
            ),
            "pattern": "SUBJECT_OBJECT_ACTION"
        }

    # Pattern 3: Subject + Object + WANT

    if middle_role == "OBJECT" and action_gloss == "WANT":
        allowed_objects = action.get("allowed_objects", [])

        if middle.get("concept") not in allowed_objects:
            return unknown_result()

        sinhala_subject = (
            "මට" if subject_gloss == "I"
            else "ඔයාට"
        )

        return {
            "english": (
                f"{english_subject} want "
                f"{middle['english']}."
            ),
            "sinhala": (
                f"{sinhala_subject} "
                f"{middle['sinhala']} ඕනේ."
            ),
            "pattern": "SUBJECT_OBJECT_WANT"
        }

    # Safe fallback for unsupported grammar patterns.
    return unknown_result()
