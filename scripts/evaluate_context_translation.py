
import json
from datetime import datetime
from pathlib import Path

from src.translation.app import translate_signs
from src.translation.translation_pipeline import (
    translate_topk_sequence,
)


def sign(*candidates):
    return {
        "top_k": [
            {"gloss": gloss, "score": score}
            for gloss, score in candidates
        ]
    }


CASES = [
    {
        "name": "Subject pronoun disambiguation",
        "mode": "topk",
        "input": [
            sign(("ME", 0.85), ("I", 0.80)),
            sign(("GO", 0.95)),
            sign(("SCHOOL", 0.92)),
        ],
        "expected_status": "SUCCESS",
        "expected_glosses": ["I", "GO", "SCHOOL"],
        "expected_english": "I am going to school.",
        "expected_sinhala": "මම පාසලට යනවා.",
    },
    {
        "name": "Possessive versus subject",
        "mode": "topk",
        "input": [
            sign(("MINE", 0.91), ("I", 0.70)),
            sign(("FOOD", 0.95)),
            sign(("EAT", 0.94)),
        ],
        "expected_status": "SUCCESS",
        "expected_glosses": ["I", "FOOD", "EAT"],
        "expected_english": "I eat food.",
        "expected_sinhala": "මම ආහාර කනවා.",
    },
    {
        "name": "Person versus temporal meaning",
        "mode": "topk",
        "input": [
            sign(("I", 0.95)),
            sign(("SEE", 0.93)),
            sign(
                ("FRIDAY", 0.88),
                ("FRIEND", 0.75),
                ("FEBRUARY", 0.65),
            ),
        ],
        "expected_status": "SUCCESS",
        "expected_glosses": ["I", "SEE", "FRIEND"],
        "expected_english": "I see a friend.",
        "expected_sinhala": "මම මිතුරාව දකිනවා.",
    },
    {
        "name": "Direct object-action translation",
        "mode": "direct",
        "input": ["YOU", "WATER", "DRINK"],
        "expected_status": "SUCCESS",
        "expected_english": "You drink water.",
        "expected_sinhala": "ඔයා වතුර බොනවා.",
    },
    {
        "name": "Temporal bilingual translation",
        "mode": "direct",
        "input": ["I", "SCHOOL", "GO", "FRIDAY"],
        "expected_status": "SUCCESS",
        "expected_english": "I am going to school on Friday.",
        "expected_sinhala": "මම සිකුරාදා පාසලට යනවා.",
    },
    {
        "name": "Insufficient context",
        "mode": "topk",
        "input": [
            sign(("ME", 0.85), ("I", 0.80)),
            sign(("WATER", 0.95)),
        ],
        "expected_status": "AMBIGUOUS",
    },
    {
        "name": "Unsupported sentence pattern",
        "mode": "direct",
        "input": ["I", "SCHOOL", "EAT"],
        "expected_status": "UNSUPPORTED_PATTERN",
    },
]


def evaluate_case(case):
    if case["mode"] == "topk":
        result = translate_topk_sequence(case["input"])
        status = result["status"]
    else:
        result = translate_signs(case["input"])
        status = (
            "UNSUPPORTED_PATTERN"
            if result["pattern"] == "UNKNOWN"
            else "SUCCESS"
        )

    checks = {
        "status": status == case["expected_status"]
    }

    if "expected_glosses" in case:
        checks["selected_glosses"] = (
            result.get("selected_glosses")
            == case["expected_glosses"]
        )

    if "expected_english" in case:
        checks["english"] = (
            result.get("english")
            == case["expected_english"]
        )

    if "expected_sinhala" in case:
        checks["sinhala"] = (
            result.get("sinhala")
            == case["expected_sinhala"]
        )

    return {
        "name": case["name"],
        "mode": case["mode"],
        "passed": all(checks.values()),
        "checks": checks,
        "actual_status": status,
        "actual_english": result.get("english"),
        "actual_sinhala": result.get("sinhala"),
        "decisions": result.get("decisions", []),
    }


def main():
    evaluations = [evaluate_case(case) for case in CASES]

    passed = sum(item["passed"] for item in evaluations)

    report = {
        "description": (
            "Functional evaluation using simulated Top-K "
            "inputs and prototype reference sentences. "
            "Not a measurement of real SLSL accuracy."
        ),
        "created_at": datetime.now().isoformat(),
        "total": len(evaluations),
        "passed": passed,
        "results": evaluations,
    }

    output_dir = Path("results/contextual_evaluation")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "pp1_functional_results.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print("\nSLSL CONTEXT-AWARE TRANSLATION EVALUATION")
    print("-" * 50)

    for item in evaluations:
        state = "PASS" if item["passed"] else "FAIL"
        print(f"[{state}] {item['name']}")

        if not item["passed"]:
            print("  Checks:", item["checks"])

    print("-" * 50)
    print(f"Passed: {passed}/{len(evaluations)}")
    print(f"Report saved to: {output_path}")


if __name__ == "__main__":
    main()
