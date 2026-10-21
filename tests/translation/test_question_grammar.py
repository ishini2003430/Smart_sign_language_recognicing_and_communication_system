
import unittest

from src.translation.app import translate_signs


class TestQuestionGrammar(unittest.TestCase):

    def test_why_want_water(self):
        result = translate_signs(
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

    def test_why_go_school(self):
        result = translate_signs(
            ["YOU", "SCHOOL", "GO", "WHY"]
        )

        self.assertEqual(
            result["english"],
            "Why are you going to school?"
        )

    def test_how_come_home(self):
        result = translate_signs(
            ["YOU", "HOME", "COME", "HOW"]
        )

        self.assertEqual(
            result["english"],
            "How are you coming home?"
        )

    def test_why_am_i_going(self):
        result = translate_signs(
            ["I", "SCHOOL", "GO", "WHY"]
        )

        self.assertEqual(
            result["english"],
            "Why am I going to school?"
        )

    def test_unsupported_question(self):
        result = translate_signs(
            ["I", "WATER", "DRINK", "HOW"]
        )

        self.assertEqual(
            result["pattern"],
            "UNKNOWN"
        )


if __name__ == "__main__":
    unittest.main()
