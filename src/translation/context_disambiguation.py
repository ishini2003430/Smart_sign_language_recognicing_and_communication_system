
import json
from pathlib import Path


DATA_PATH = Path(__file__).with_name("ambiguity_groups.json")


def load_ambiguity_groups():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["groups"]


def find_ambiguity_group(sign_form):
    """Find an ambiguity group by its shared sign-form ID."""
    sign_form = sign_form.strip().upper()

    for group in load_ambiguity_groups():
        if group["form_id"].upper() == sign_form:
            return group

    return None


def disambiguate_sign(sign_form, expected_semantic_type=None):
    """
    Select a meaning using an explicitly supplied contextual constraint.

    This first prototype does not infer context automatically.
    """

    group = find_ambiguity_group(sign_form)

    if group is None:
        return {
            "status": "UNKNOWN_SIGN_FORM",
            "selected_meaning": None,
            "candidates": [],
            "reason": "No ambiguity group found for this sign form."
        }

    candidates = group["meanings"]

    if expected_semantic_type is None:
        return {
            "status": "AMBIGUOUS",
            "selected_meaning": None,
            "candidates": candidates,
            "reason": "No contextual semantic type was provided."
        }

    expected_type = expected_semantic_type.strip().upper()

    matches = [
        candidate
        for candidate in candidates
        if candidate["semantic_type"].upper() == expected_type
    ]

    if len(matches) == 1:
        return {
            "status": "RESOLVED",
            "selected_meaning": matches[0],
            "candidates": candidates,
            "reason": f"Context requires semantic type {expected_type}."
        }

        return {
        "status": "AMBIGUOUS",
        "selected_meaning": None,
        "candidates": candidates,
        "reason": (
            f"Context type {expected_type} did not identify "
            "exactly one meaning."
        )
    }
