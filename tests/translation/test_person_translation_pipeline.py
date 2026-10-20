
import unittest

from src.translation.app import translate_signs
from src.translation.translation_pipeline import (
    translate_topk_sequence
)


class TestPersonTranslationPipeline(unittest.TestCase):

    def test_direct_see_friend(self):
        result = translate_signs(
            ["I", "SEE", "FRIEND"]
        )

        self.assertEqual(
            result["english"],
            "I see a friend."
        )
        self.assertEqual(
            result["sinhala"],
            "මම මිතුරාව දකිනවා."
        )

    def test_direct_alternative_order(self):
        result = translate_signs(
            ["YOU", "FRIEND", "SEE"]
        )

        self.assertEqual(
            result["english"],
            "You see a friend."
        )
        self.assertEqual(
            result["sinhala"],
            "ඔයා මිතුරාව දකිනවා."
        )

    def test_context_overrides_score_and_translates(self):
        sequence = [
            {
                "top_k": [
                    {"gloss": "I", "score": 0.95}
                ]
            },
            {
                "top_k": [
                    {"gloss": "SEE", "score": 0.93}
                ]
            },
            {
                "top_k": [
                    {"gloss": "FRIDAY", "score": 0.88},
                    {"gloss": "FRIEND", "score": 0.75},
                    {"gloss": "FEBRUARY", "score": 0.65}
                ]
            }
        ]

        result = translate_topk_sequence(sequence)

        self.assertEqual(result["status"], "SUCCESS")

        self.assertEqual(
            result["selected_glosses"],
            ["I", "SEE", "FRIEND"]
        )

        self.assertEqual(
            result["english"],
            "I see a friend."
        )

        self.assertEqual(
            result["sinhala"],
            "මම මිතුරාව දකිනවා."
        )

        self.assertEqual(
            result["decisions"][2]["recognition_baseline"],
            "FRIDAY"
        )

        self.assertEqual(
            result["decisions"][2]["selected"],
            "FRIEND"
        )


if __name__ == "__main__":
    unittest.main()
