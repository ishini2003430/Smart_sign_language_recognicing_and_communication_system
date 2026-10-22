
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

    
    # Pattern: Question using WHY or HOW
    #
    # Examples:
    # YOU WATER WANT WHY
    # YOU SCHOOL GO WHY
    # YOU HOME COME HOW
    # I SCHOOL GO WHY
    #
    # The question word is the final gloss.
    # The remaining three glosses use existing grammar rules.

    if len(signs) == 4 and signs[-1] in {"WHY", "HOW"}:

        question_gloss = signs[-1]
        base_signs = signs[:3]

        if base_signs[0] not in {"I", "YOU"}:
            return unknown_result()

        base_result = reconstruct_sentence(base_signs, lexicon)

        if base_result["pattern"] == "UNKNOWN":
            return unknown_result()

        subject_gloss = base_signs[0]

        english_subject = (
            "I" if subject_gloss == "I" else "you"
        )

        english_auxiliary = (
            "am" if subject_gloss == "I" else "are"
        )

        english_base = base_result["english"].rstrip(".")
        sinhala_base = base_result["sinhala"].rstrip(".")

        # WHY + WANT:
        # "You want water." -> "Why do you want water?"
        if (
            question_gloss == "WHY"
            and base_result["pattern"] == "SUBJECT_OBJECT_WANT"
        ):
            subject_word = (
                "I" if subject_gloss == "I" else "You"
            )

            prefix = f"{subject_word} want "

            if not english_base.startswith(prefix):
                return unknown_result()

            english_object = english_base[len(prefix):]

            return {
                "english": (
                    f"Why do {english_subject} "
                    f"want {english_object}?"
                ),
                "sinhala": f"{sinhala_base} ඇයි?",
                "pattern": "QUESTION_WHY_WANT"
            }

        # WHY / HOW + GO / COME
        if base_result["pattern"] == "SUBJECT_LOCATION_ACTION":

            subject_word = (
                "I" if subject_gloss == "I" else "You"
            )

            prefix = (
                f"{subject_word} {english_auxiliary} "
            )

            if not english_base.startswith(prefix):
                return unknown_result()

            verb_phrase = english_base[len(prefix):]

            question_word = (
                "Why" if question_gloss == "WHY" else "How"
            )

            sinhala_question = (
                "ඇයි" if question_gloss == "WHY"
                else "කොහොමද"
            )
            
            # Convert Sinhala statement verbs into
            # more natural question constructions.
            #
            # යනවා -> යන්නේ
            # එනවා -> එන්නේ

            if sinhala_base.endswith("යනවා"):
                sinhala_base = (
                    sinhala_base[:-len("යනවා")] + "යන්නේ"
                )

            elif sinhala_base.endswith("එනවා"):
                sinhala_base = (
                    sinhala_base[:-len("එනවා")] + "එන්නේ"
                )


            return {
                "english": (
                    f"{question_word} {english_auxiliary} "
                    f"{english_subject} {verb_phrase}?"
                ),
                "sinhala": (
                    f"{sinhala_base} {sinhala_question}?"
                ),
                "pattern": (
                    f"QUESTION_{question_gloss}_MOVEMENT"
                )
            }

        return unknown_result()


    
    # Pattern: Person + Location + GO / COME
    #
    # Examples:
    # MOTHER HOME COME
    # FATHER SCHOOL GO
    # SISTER GO HOME
    #
    # Supports both action-location and location-action orders.

    family_subjects = {
        "MOTHER",
        "FATHER",
        "DAUGHTER",
        "SON",
        "BROTHER",
        "SISTER",
        "FRIEND"
    }

    if len(signs) == 3 and signs[0] in family_subjects:

        subject_gloss = signs[0]

        if subject_gloss not in lexicon:
            return unknown_result()

        subject = lexicon[subject_gloss]

        # Identify the location and action.
        if signs[1] in {"GO", "COME"}:
            action_gloss = signs[1]
            location_gloss = signs[2]
        else:
            location_gloss = signs[1]
            action_gloss = signs[2]

        if (
            location_gloss in lexicon
            and action_gloss in lexicon
            and lexicon[location_gloss].get("grammar_role")
                == "LOCATION"
            and action_gloss in {"GO", "COME"}
        ):

            english_locations = {
                "SCHOOL": "to school",
                "HOME": "home",
                "COLOMBO": "to Colombo"
            }

            sinhala_locations = {
                "SCHOOL": "පාසලට",
                "HOME": "ගෙදර",
                "COLOMBO": "කොළඹට"
            }

            if location_gloss not in english_locations:
                return unknown_result()

            english_subject = subject["english"].capitalize()
            sinhala_subject = subject["sinhala"]

            english_verb = (
                "is going"
                if action_gloss == "GO"
                else "is coming"
            )

            sinhala_verb = (
                "යනවා"
                if action_gloss == "GO"
                else "එනවා"
            )

            return {
                "english": (
                    f"{english_subject} {english_verb} "
                    f"{english_locations[location_gloss]}."
                ),
                "sinhala": (
                    f"{sinhala_subject} "
                    f"{sinhala_locations[location_gloss]} "
                    f"{sinhala_verb}."
                ),
                "pattern": "PERSON_LOCATION_ACTION"
            }


        # Handle a four-gloss sentence with an explicit time expression.
    if len(signs) == 4:
        time_gloss = signs[-1]

        time_forms = {
            "FRIDAY": {
                "english": "on Friday",
                "sinhala": "සිකුරාදා"
            },
            "FEBRUARY": {
                "english": "in February",
                "sinhala": "පෙබරවාරි මාසයේ"
            }
        }

        if time_gloss not in time_forms:
            return unknown_result()

        # Reuse the existing three-word grammar engine.
        base_result = reconstruct_sentence(signs[:3], lexicon)

        if base_result["pattern"] != "SUBJECT_LOCATION_ACTION":
            return unknown_result()

        english_base = base_result["english"].rstrip(".")
        time_phrase = time_forms[time_gloss]

        # Place the time expression after the location in English.
        english = (
            f"{english_base} {time_phrase['english']}."
        )

        # In this prototype, place the time expression
        # after the subject in the Sinhala sentence.
        if signs[0] == "I":
            sinhala_subject = "මම"
        elif signs[0] == "YOU":
            sinhala_subject = "ඔයා"
        else:
            return unknown_result()

        sinhala_base = base_result["sinhala"].rstrip(".")
        subject_prefix = sinhala_subject + " "

        if not sinhala_base.startswith(subject_prefix):
            return unknown_result()

        remainder = sinhala_base[len(subject_prefix):]

        sinhala = (
            f"{sinhala_subject} "
            f"{time_phrase['sinhala']} {remainder}."
        )

        return {
            "english": english,
            "sinhala": sinhala,
            "pattern": "SUBJECT_LOCATION_ACTION_TIME"
        }

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

    
    # Pattern: Subject + Person + SEE / KNOW
    #
    # Supported word orders:
    # I FATHER SEE
    # I SEE FATHER
    #
    # Applies to all registered person concepts.

    if (
        middle.get("category") == "PERSON"
        and action_gloss in {"SEE", "KNOW"}
    ):
        sinhala_person_objects = {
            "MOTHER": "අම්මාව",
            "FATHER": "තාත්තාව",
            "DAUGHTER": "දුවව",
            "SON": "පුතාව",
            "BROTHER": "සහෝදරයාව",
            "SISTER": "සහෝදරියව",
            "FRIEND": "මිතුරාව"
        }

        sinhala_object = sinhala_person_objects.get(
            middle_gloss
        )

        if sinhala_object is None:
            return unknown_result()

        english_action = {
            "SEE": "see",
            "KNOW": "know"
        }[action_gloss]

        sinhala_action = {
            "SEE": "දකිනවා",
            "KNOW": "දන්නවා"
        }[action_gloss]

        return {
            "english": (
                f"{english_subject} {english_action} "
                f"a {middle['english']}."
            ),
            "sinhala": (
                f"{sinhala_subject} "
                f"{sinhala_object} {sinhala_action}."
            ),
            "pattern": "SUBJECT_PERSON_COGNITIVE_ACTION"
        }

    
    # Pattern: Subject + LOOK + Location
    #
    # Supports:
    # I LOOK SCHOOL
    # YOU HOME LOOK
    # I LOOK COLOMBO

    if middle_role == "LOCATION" and action_gloss == "LOOK":

        location_forms = {
            "SCHOOL": {
                "english": "the school",
                "sinhala": "පාසල"
            },
            "HOME": {
                "english": "the home",
                "sinhala": "ගෙදර"
            },
            "COLOMBO": {
                "english": "Colombo",
                "sinhala": "කොළඹ"
            }
        }

        if middle_gloss not in location_forms:
            return unknown_result()

        location = location_forms[middle_gloss]

        return {
            "english": (
                f"{english_subject} look at "
                f"{location['english']}."
            ),
            "sinhala": (
                f"{sinhala_subject} "
                f"{location['sinhala']} දිහා බලනවා."
            ),
            "pattern": "SUBJECT_LOOK_LOCATION"
        }



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

        elif middle_gloss == "COLOMBO":
            english_location = "to Colombo"
            sinhala_location = "කොළඹට"
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
        
    # Pattern: Subject + SEE + Person
    # Supports both:
    # I + SEE + FRIEND
    # I + FRIEND + SEE

    if (
        middle_role == "PERSON"
        and action_gloss == "SEE"
    ):
        allowed_objects = action.get("allowed_objects", [])

        if middle.get("concept") not in allowed_objects:
            return unknown_result()

        english_person = middle["english"]
        sinhala_person = middle["sinhala"]

        # Explicitly supported Sinhala object forms
        sinhala_object_forms = {
            "FRIEND": "මිතුරාව"
        }

        sinhala_object = sinhala_object_forms.get(
            middle_gloss
        )

        if sinhala_object is None:
            return unknown_result()

        return {
            "english": (
                f"{english_subject} see a "
                f"{english_person}."
            ),
            "sinhala": (
                f"{sinhala_subject} "
                f"{sinhala_object} දකිනවා."
            ),
            "pattern": "SUBJECT_PERSON_ACTION"
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
