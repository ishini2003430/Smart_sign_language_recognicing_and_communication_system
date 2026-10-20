
import json
from pathlib import Path


LEXICON_PATH = Path(__file__).with_name("lexicon.json")


def load_lexicon():
    with open(LEXICON_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def analyze_context(signs):
    """
    Extract contextual features from surrounding glosses.

    This function does not choose an ambiguous meaning.
    It identifies known grammatical roles and concepts.
    """
    lexicon = load_lexicon()

    normalized_signs = [
        sign.strip().upper()
        for sign in signs
    ]

    features = {
        "signs": normalized_signs,
        "subjects": [],
        "actions": [],
        "locations": [],
        "objects": [],
        "other_known_signs": [],
        "unknown_signs": []
    }

    for position, gloss in enumerate(normalized_signs):
        entry = lexicon.get(gloss)

        if entry is None:
            features["unknown_signs"].append({
                "gloss": gloss,
                "position": position
            })
            continue

        sign_info = {
            "gloss": gloss,
            "concept": entry.get("concept"),
            "position": position
        }

        role = entry.get("grammar_role")

        if role == "SUBJECT":
            features["subjects"].append(sign_info)
        elif role == "ACTION":
            features["actions"].append(sign_info)
        elif role == "LOCATION":
            features["locations"].append(sign_info)
        elif role == "OBJECT":
            features["objects"].append(sign_info)
        else:
            features["other_known_signs"].append(sign_info)

    return features
