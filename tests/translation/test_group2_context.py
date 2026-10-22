
import unittest

from src.translation.app import translate_signs
from src.translation.translation_pipeline import (
    translate_topk_sequence
)


class TestGroup2Context(unittest.TestCase):

    def test_direct_colombo_translation(self):
        result = translate_signs(
            ["I", "COLOMBO", "GO"]
        )

        self.assertEqual(
            result["english"],
            "I am going to Colombo."
        )

        self.assertEqual(
            result["sinhala"],
            "මම කොළඹට යනවා."
        )

    def test_context_selects_colombo(self):
        sequence = [
            {
                "top_k": [
                    {"gloss": "I", "score": 0.95}
                ]
            },
            {
                "top_k": [
                    {"gloss": "LOOK", "score": 0.85},
                    {"gloss": "CANCER", "score": 0.80},
                    {"gloss": "COLOMBO", "score": 0.70},
                    {"gloss": "SEE", "score": 0.65}
                ]
            },
            {
                "top_k": [
                    {"gloss": "GO", "score": 0.90}
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
            ["I", "COLOMBO", "GO"]
        )

        self.assertEqual(
            result["english"],
            "I am going to Colombo."
        )

        decision = result["decisions"][1]

        self.assertEqual(
            decision["recognition_baseline"],
            "LOOK"
        )

        self.assertEqual(
            decision["selected"],
            "COLOMBO"
        )

        self.assertTrue(
            decision["context_overrode_recognition"]
        )

    def test_family_member_goes_to_colombo(self):
        result = translate_signs(
            ["MOTHER", "COLOMBO", "GO"]
        )

        self.assertEqual(
            result["english"],
            "Mother is going to Colombo."
        )

        self.assertEqual(
            result["sinhala"],
            "අම්මා කොළඹට යනවා."
        )


if __name__ == "__main__":
    unittest.main()
