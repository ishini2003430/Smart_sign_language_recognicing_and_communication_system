
import unittest

from src.translation.translation_pipeline import (
    translate_topk_sequence
)


class TestQuestionTopK(unittest.TestCase):

    def test_why_overrides_higher_how_score(self):
        sequence = [
            {
                "top_k": [
                    {"gloss": "YOU", "score": 0.95}
                ]
            },
            {
                "top_k": [
                    {"gloss": "WATER", "score": 0.92}
                ]
            },
            {
                "top_k": [
                    {"gloss": "WANT", "score": 0.90}
                ]
            },
            {
                "top_k": [
                    {"gloss": "HOW", "score": 0.85},
                    {"gloss": "WHY", "score": 0.70}
                ]
            }
        ]

        result = translate_topk_sequence(sequence)

        self.assertEqual(
            result["status"],
            "SUCCESS"
        )

        self.assertEqual(
            result["selected_glosses"],
            ["YOU", "WATER", "WANT", "WHY"]
        )

        self.assertEqual(
            result["english"],
            "Why do you want water?"
        )

        self.assertEqual(
            result["sinhala"],
            "ඔයාට වතුර ඕනේ ඇයි?"
        )

        question_decision = result["decisions"][3]

        self.assertEqual(
            question_decision["recognition_baseline"],
            "HOW"
        )

        self.assertEqual(
            question_decision["selected"],
            "WHY"
        )

        self.assertTrue(
            question_decision["context_overrode_recognition"]
        )

    def test_both_valid_questions_remain_ambiguous(self):
        sequence = [
            {
                "top_k": [
                    {"gloss": "YOU", "score": 0.95}
                ]
            },
            {
                "top_k": [
                    {"gloss": "SCHOOL", "score": 0.92}
                ]
            },
            {
                "top_k": [
                    {"gloss": "GO", "score": 0.90}
                ]
            },
            {
                "top_k": [
                    {"gloss": "HOW", "score": 0.85},
                    {"gloss": "WHY", "score": 0.70}
                ]
            }
        ]

        result = translate_topk_sequence(sequence)

        self.assertEqual(
            result["status"],
            "AMBIGUOUS"
        )


if __name__ == "__main__":
    unittest.main()
