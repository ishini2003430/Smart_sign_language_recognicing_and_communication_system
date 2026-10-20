
import unittest

from src.translation.app import translate_signs


class TestExtendedGrammar(unittest.TestCase):

    def test_subject_action_location_order(self):
        result = translate_signs(["I", "GO", "SCHOOL"])

        self.assertEqual(
            result["english"],
            "I am going to school."
        )
        self.assertEqual(
            result["sinhala"],
            "මම පාසලට යනවා."
        )

    def test_subject_action_object_order(self):
        result = translate_signs(["YOU", "DRINK", "WATER"])

        self.assertEqual(
            result["english"],
            "You drink water."
        )

    def test_want_water(self):
        result = translate_signs(["I", "WATER", "WANT"])

        self.assertEqual(
            result["english"],
            "I want water."
        )
        self.assertEqual(
            result["sinhala"],
            "මට වතුර ඕනේ."
        )

    def test_come_home(self):
        result = translate_signs(["I", "HOME", "COME"])

        self.assertEqual(
            result["english"],
            "I am coming home."
        )
        self.assertEqual(
            result["sinhala"],
            "මම ගෙදර එනවා."
        )

    def test_unsupported_action_object(self):
        result = translate_signs(["I", "SCHOOL", "EAT"])

        self.assertEqual(result["pattern"], "UNKNOWN")
        self.assertIsNone(result["english"])

    def test_different_subject(self):
        result = translate_signs(["YOU", "FOOD", "EAT"])

        self.assertEqual(
            result["english"],
            "You eat food."
        )
        self.assertEqual(
            result["sinhala"],
            "ඔයා ආහාර කනවා."
        )


if __name__ == "__main__":
    unittest.main()
