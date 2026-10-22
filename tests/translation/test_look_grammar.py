
import unittest

from src.translation.app import translate_signs


class TestLookGrammar(unittest.TestCase):

    def test_look_at_school(self):
        result = translate_signs(
            ["I", "LOOK", "SCHOOL"]
        )

        self.assertEqual(
            result["english"],
            "I look at the school."
        )

        self.assertEqual(
            result["sinhala"],
            "මම පාසල දිහා බලනවා."
        )

    def test_look_at_home(self):
        result = translate_signs(
            ["YOU", "HOME", "LOOK"]
        )

        self.assertEqual(
            result["english"],
            "You look at the home."
        )

    def test_look_at_colombo(self):
        result = translate_signs(
            ["I", "LOOK", "COLOMBO"]
        )

        self.assertEqual(
            result["english"],
            "I look at Colombo."
        )

    def test_unsupported_look_object(self):
        result = translate_signs(
            ["I", "WATER", "LOOK"]
        )

        self.assertEqual(
            result["pattern"],
            "UNKNOWN"
        )


if __name__ == "__main__":
    unittest.main()
