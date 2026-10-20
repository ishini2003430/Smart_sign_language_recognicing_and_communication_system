
import unittest

from src.translation.topk_context_selector import (
    select_candidate
)


class TestTopKContextSelector(unittest.TestCase):

    def test_context_overrides_recognition_score(self):
        sequence = [
            {
                "top_k": [
                    {"gloss": "ME", "score": 0.85},
                    {"gloss": "I", "score": 0.80}
                ]
            },
            {
                "top_k": [
                    {"gloss": "GO", "score": 0.95}
                ]
            },
            {
                "top_k": [
                    {"gloss": "SCHOOL", "score": 0.92}
                ]
            }
        ]

        result = select_candidate(
            sequence,
            ambiguous_position=0
        )

        self.assertEqual(result["status"], "RESOLVED")
        self.assertEqual(result["selected"], "I")
        self.assertEqual(
            result["recognition_baseline"],
            "ME"
        )

    def test_insufficient_context(self):
        sequence = [
            {
                "top_k": [
                    {"gloss": "ME", "score": 0.85},
                    {"gloss": "I", "score": 0.80}
                ]
            },
            {
                "top_k": [
                    {"gloss": "WATER", "score": 0.95}
                ]
            }
        ]

        result = select_candidate(
            sequence,
            ambiguous_position=0
        )

        self.assertEqual(result["status"], "AMBIGUOUS")
        self.assertIsNone(result["selected"])


if __name__ == "__main__":
    unittest.main()
