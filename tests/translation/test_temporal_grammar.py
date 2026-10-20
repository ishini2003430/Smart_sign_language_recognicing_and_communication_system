
import unittest

from src.translation.app import translate_signs


class TestTemporalGrammar(unittest.TestCase):

    def test_friday_school(self):
        result = translate_signs(
            ["I", "SCHOOL", "GO", "FRIDAY"]
        )

        self.assertEqual(
            result["english"],
            "I am going to school on Friday."
        )

        self.assertEqual(
            result["sinhala"],
            "මම සිකුරාදා පාසලට යනවා."
        )

    def test_alternative_word_order(self):
        result = translate_signs(
            ["YOU", "GO", "SCHOOL", "FRIDAY"]
        )

        self.assertEqual(
            result["english"],
            "You are going to school on Friday."
        )

    def test_february_home(self):
        result = translate_signs(
            ["I", "HOME", "COME", "FEBRUARY"]
        )

        self.assertEqual(
            result["english"],
            "I am coming home in February."
        )

        self.assertEqual(
            result["sinhala"],
            "මම පෙබරවාරි මාසයේ ගෙදර එනවා."
        )

    def test_unknown_time(self):
        result = translate_signs(
            ["I", "SCHOOL", "GO", "UNKNOWN_TIME"]
        )

        self.assertEqual(result["pattern"], "UNKNOWN")
        self.assertIsNone(result["english"])

    def test_existing_three_word_rule_preserved(self):
        result = translate_signs(
            ["I", "SCHOOL", "GO"]
        )

        self.assertEqual(
            result["english"],
            "I am going to school."
        )


if __name__ == "__main__":
    unittest.main()
