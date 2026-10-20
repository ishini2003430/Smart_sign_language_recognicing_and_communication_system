
import unittest

from src.translation.translation_pipeline import (
    translate_topk_sequence
)


class TestFullSequenceRanking(unittest.TestCase):

    def test_two_ambiguous_positions(self):
        sequence = [
            {
                "top_k": [
                    {"gloss": "ME", "score": 0.85},
                    {"gloss": "I", "score": 0.80}
                ]
            },
            {
                "top_k": [
                    {"gloss": "GO", "score": 0.90},
                    {"gloss": "DRINK", "score": 0.75}
                ]
            },
            {
                "top_k": [
                    {"gloss": "SCHOOL", "score": 0.92}
                ]
            }
        ]

        result = translate_topk_sequence(sequence)

        self.assertEqual(result["status"], "SUCCESS")
        self.assertEqual(
            result["selected_glosses"],
            ["I", "GO", "SCHOOL"]
        )
        self.assertEqual(
            result["english"],
            "I am going to school."
        )
        self.assertEqual(
            result["sinhala"],
            "මම පාසලට යනවා."
        )

    def test_multiple_valid_interpretations(self):
        sequence = [
            {
                "top_k": [
                    {"gloss": "I", "score": 0.80},
                    {"gloss": "YOU", "score": 0.75}
                ]
            },
            {
                "top_k": [
                    {"gloss": "GO", "score": 0.90},
                    {"gloss": "COME", "score": 0.80}
                ]
            },
            {
                "top_k": [
                    {"gloss": "SCHOOL", "score": 0.92}
                ]
            }
        ]

        result = translate_topk_sequence(sequence)

        self.assertEqual(
            result["status"],
            "AMBIGUOUS"
        )

    def test_no_supported_interpretation(self):
        sequence = [
            {
                "top_k": [
                    {"gloss": "ME", "score": 0.90},
                    {"gloss": "MINE", "score": 0.80}
                ]
            },
            {
                "top_k": [
                    {"gloss": "EAT", "score": 0.95},
                    {"gloss": "DRINK", "score": 0.80}
                ]
            },
            {
                "top_k": [
                    {"gloss": "SCHOOL", "score": 0.90}
                ]
            }
        ]

        result = translate_topk_sequence(sequence)

        self.assertEqual(
            result["status"],
            "UNSUPPORTED_PATTERN"
        )


if __name__ == "__main__":
    unittest.main()
