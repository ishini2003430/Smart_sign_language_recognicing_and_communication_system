
import json
from pathlib import Path
from .sentence_rules import reconstruct_sentence


# Load the SLSL vocabulary
LEXICON_PATH = Path(__file__).with_name("lexicon.json")

with open(LEXICON_PATH, "r", encoding="utf-8") as file:
    lexicon = json.load(file)


def translate_signs(signs):
    # Normalize recognized glosses
    signs = [sign.upper().strip() for sign in signs]

    # Map glosses to concepts
    mapped_signs = []

    for sign in signs:
        if sign in lexicon:
            mapped_signs.append({
                "gloss": sign,
                **lexicon[sign]
            })
        else:
            mapped_signs.append({
                "gloss": sign,
                "concept": "UNKNOWN",
                "english": sign,
                "sinhala": "නොදන්නා ලකුණ",
                "category": "UNKNOWN"
            })

    # Use the sentence reconstruction engine
    translation = reconstruct_sentence(signs, lexicon)

    return {
        "english": translation["english"],
        "sinhala": translation["sinhala"],
        "pattern": translation["pattern"],
        "mapped_signs": mapped_signs
    }


if __name__ == "__main__":
    test_signs = ["I", "SCHOOL", "GO"]

    result = translate_signs(test_signs)

    print("Recognized signs:", test_signs)
    print("\nConcept mapping:")

    for item in result["mapped_signs"]:
        print(f'{item["gloss"]} -> {item["concept"]}')

    print("\nMatched pattern:", result["pattern"])
    print("English:", result["english"])
    print("Sinhala:", result["sinhala"])
