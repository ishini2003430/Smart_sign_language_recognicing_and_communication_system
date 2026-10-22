"""
evaluate.py
===========
Evaluation helpers for the sign animation component.

Current scope
-------------
- Measure pipeline coverage on a set of test sentences.
- Report missing signs so vocabulary gaps can be flagged to the expert team.
- (Future) Calculate meaning-preservation metrics once expert annotations
  are available.

Run this script directly:
    python -m src.sign_animation.evaluate

Or import its functions in research notebooks.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# Allow running as a script from the repository root.
_REPO_ROOT = Path(__file__).parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.sign_animation.animation_service import AnimationService


@dataclass
class EvaluationReport:
    """Summary of an evaluation run."""

    total_sentences: int = 0
    total_tokens: int = 0
    covered_tokens: int = 0
    uncovered_tokens: int = 0
    missing_token_counts: dict[str, int] = field(default_factory=dict)
    coverage_per_sentence: list[float] = field(default_factory=list)

    @property
    def overall_coverage(self) -> float:
        if self.total_tokens == 0:
            return 0.0
        return self.covered_tokens / self.total_tokens

    def to_dict(self) -> dict:
        return {
            "total_sentences": self.total_sentences,
            "total_tokens": self.total_tokens,
            "covered_tokens": self.covered_tokens,
            "uncovered_tokens": self.uncovered_tokens,
            "overall_coverage": round(self.overall_coverage, 4),
            "missing_token_counts": dict(
                sorted(
                    self.missing_token_counts.items(),
                    key=lambda x: x[1],
                    reverse=True,
                )
            ),
            "coverage_per_sentence": [
                round(c, 4) for c in self.coverage_per_sentence
            ],
        }


def evaluate_sentences(
    sentences: list[str],
    service: Optional[AnimationService] = None,
) -> EvaluationReport:
    """
    Evaluate pipeline coverage on *sentences*.

    Parameters
    ----------
    sentences:
        List of text strings to translate.
    service:
        An initialised AnimationService.  Created from defaults if None.

    Returns
    -------
    EvaluationReport
    """
    if service is None:
        service = AnimationService.create()

    report = EvaluationReport()

    for sentence in sentences:
        result = service.translate(sentence)
        report.total_sentences += 1
        n_tokens = len(result.tokens)
        n_found = len(result.playback_sequence)
        n_missing = len(result.missing_tokens)

        report.total_tokens += n_tokens
        report.covered_tokens += n_found
        report.uncovered_tokens += n_missing

        for tok in result.missing_tokens:
            report.missing_token_counts[tok] = (
                report.missing_token_counts.get(tok, 0) + 1
            )

        coverage = n_found / n_tokens if n_tokens > 0 else 0.0
        report.coverage_per_sentence.append(coverage)

    return report


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

_DEFAULT_EVAL_SENTENCES = [
    "I want water",
    "mother go hospital",
    "eat food today",
    "I need medicine",
    "come home tomorrow",
    "I want food",
    "mother drink water",
    "doctor come today",
]


def main() -> None:
    print("=== Sign Animation Evaluation ===\n")

    try:
        service = AnimationService.create()
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}")
        print(
            "\nHint: Create dataset/metadata/signs.json first "
            "(see docs/SIGN_ANIMATION.md for the format)."
        )
        sys.exit(1)

    report = evaluate_sentences(_DEFAULT_EVAL_SENTENCES, service)
    print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
