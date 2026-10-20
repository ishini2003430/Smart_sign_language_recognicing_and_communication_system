
def reconstruct_sentence(signs, lexicon):
    """
    Reconstruct bilingual sentences from glosses
    using lexicon data and supported grammar patterns.
    """

    signs = [sign.upper().strip() for sign in signs]

    # Reject empty input, unknown glosses, or incorrect sequence length.
    if not signs or any(sign not in lexicon for sign in signs):
        return {"english": None, "sinhala": None, "pattern": "UNKNOWN"}

    if len(signs) != 3:
        return {"english": None, "sinhala": None, "pattern": "UNKNOWN"}

    subject, middle, action = [lexicon[sign] for sign in signs]

    # Confirm the expected grammatical roles.
    if subject.get("grammar_role") != "SUBJECT":
        return {"english": None, "sinhala": None, "pattern": "UNKNOWN"}

    if action.get("grammar_role") != "ACTION":
        return {"english": None, "sinhala": None, "pattern": "UNKNOWN"}

    # Pattern 1: Subject + Location + GO
    if middle.get("grammar_role") == "LOCATION" and signs[2] == "GO":
        # Explicit language-specific forms for this supported pattern.
        if signs[0] == "I":
            english_subject = "I"
            english_verb = "am going"
            sinhala_subject = "මම"
        elif signs[0] == "YOU":
            english_subject = "You"
            english_verb = "are going"
            sinhala_subject = subject["sinhala"]
        else:
            return {"english": None, "sinhala": None, "pattern": "UNKNOWN"}

        if signs[1] == "SCHOOL":
            english_location = "to school"
            sinhala_location = "පාසලට"
        elif signs[1] == "HOME":
            english_location = "home"
            sinhala_location = "ගෙදර"
        else:
            return {"english": None, "sinhala": None, "pattern": "UNKNOWN"}

        english = f"{english_subject} {english_verb} {english_location}."
        sinhala = f"{sinhala_subject} {sinhala_location} යනවා."

        return {
            "english": english,
            "sinhala": sinhala,
            "pattern": "SUBJECT_LOCATION_ACTION"
        }

    
    # Pattern 2: Subject + Object + Action
    if (
        subject.get("grammar_role") == "SUBJECT"
        and middle.get("grammar_role") == "OBJECT"
        and action.get("grammar_role") == "ACTION"
    ):
        # Only actions with the appropriate object-taking behaviour
        # should be used in this pattern.
        allowed_objects = action.get("allowed_objects", [])
        if middle["concept"] not in allowed_objects:
            return {
                "english": None,
                "sinhala": None,
                "pattern": "UNKNOWN"
            }

        english_subject = subject["english"].capitalize()
        english_object = middle["english"]
        english_action = action["english"]

        english = (
            f"{english_subject} {english_action} {english_object}."
        )

        sinhala = (
            f"{subject['sinhala']} "
            f"{middle['sinhala']} "
            f"{action['sinhala']}."
        )

        return {
            "english": english,
            "sinhala": sinhala,
            "pattern": "SUBJECT_OBJECT_ACTION"
        }

            # No supported grammatical pattern matched
    return {
        "english": None,
        "sinhala": None,
        "pattern": "UNKNOWN"
    }

