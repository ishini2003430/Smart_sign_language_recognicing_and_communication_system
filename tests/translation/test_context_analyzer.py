
import unittest

from src.translation.context_analyzer import analyze_context


class TestContextAnalyzer(unittest.TestCase):

    def test_extracts_sentence_features(self):
        result = analyze_context(
            ["I", "SCHOOL", "GO", "SIGN_FORM_G01"]
        )

        self.assertEqual(
            result["subjects"][0]["gloss"],
            "I"
        )
        self.assertEqual(
            result["locations"][0]["gloss"],
            "SCHOOL"
        )
        self.assertEqual(
            result["actions"][0]["gloss"],
            "GO"
        )

    def test_unknown_sign_is_preserved(self):
        result = analyze_context(
            ["I", "SIGN_FORM_G01", "GO"]
        )

        self.assertEqual(
            result["unknown_signs"][0]["gloss"],
            "SIGN_FORM_G01"
        )
        self.assertEqual(
            result["unknown_signs"][0]["position"],
            1
        )

    def test_normalization(self):
        result = analyze_context(
            [" i ", " school ", " go "]
        )

        self.assertEqual(
            result["signs"],
            ["I", "SCHOOL", "GO"]
        )


if __name__ == "__main__":
    unittest.main()
