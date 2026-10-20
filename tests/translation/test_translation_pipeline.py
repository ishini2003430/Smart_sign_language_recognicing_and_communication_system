
import unittest

from src.translation.translation_pipeline import (
    translate_topk_sequence
)


class TestTranslationPipeline(unittest.TestCase):

    def test_contextual_selection_and_translation(self):
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

        # Check whether context overrode the highest score.
        self.assertEqual(
            result["decisions"][0]["recognition_baseline"],
            "ME"
        )
        self.assertEqual(
            result["decisions"][0]["selected"],
            "I"
        )

    def test_existing_translation_pattern(self):
        sequence = [
            {"top_k": [{"gloss": "YOU", "score": 0.9}]},
            {"top_k": [{"gloss": "WATER", "score": 0.9}]},
            {"top_k": [{"gloss": "DRINK", "score": 0.9}]}
        ]

        result = translate_topk_sequence(sequence)

        self.assertEqual(result["status"], "SUCCESS")
        self.assertEqual(
            result["english"],
            "You drink water."
        )

    def test_unresolved_ambiguity(self):
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

        result = translate_topk_sequence(sequence)

        self.assertEqual(result["status"], "AMBIGUOUS")
        self.assertIsNone(result["english"])

    def test_unsupported_pattern(self):
        sequence = [
            {"top_k": [{"gloss": "I", "score": 0.9}]},
            {"top_k": [{"gloss": "SCHOOL", "score": 0.9}]},
            {"top_k": [{"gloss": "EAT", "score": 0.9}]}
        ]

        result = translate_topk_sequence(sequence)

        self.assertEqual(
            result["status"],
            "UNSUPPORTED_PATTERN"
        )
        self.assertIsNone(result["english"])


if __name__ == "__main__":
    unittest.main()
