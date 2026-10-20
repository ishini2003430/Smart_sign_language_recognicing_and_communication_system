
import unittest

from src.translation.translation_pipeline import (
    translate_topk_sequence
)


class TestContextExplanations(unittest.TestCase):

    def test_full_sequence_explains_override(self):
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

        first_decision = result["decisions"][0]

        self.assertEqual(
            first_decision["recognition_baseline"],
            "ME"
        )

        self.assertEqual(
            first_decision["selected"],
            "I"
        )

        self.assertTrue(
            first_decision["context_overrode_recognition"]
        )

        self.assertEqual(
            first_decision["selected_recognition_score"],
            0.80
        )

    def test_other_sign_not_overridden(self):
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

        self.assertFalse(
            result["decisions"][1][
                "context_overrode_recognition"
            ]
        )


if __name__ == "__main__":
    unittest.main()
