
import unittest
from src.translation.app import translate_signs


class TestTranslator(unittest.TestCase):

    def test_i_go_to_school(self):
        result = translate_signs(["I", "SCHOOL", "GO"])
        self.assertEqual(result["english"], "I am going to school.")
        self.assertEqual(result["sinhala"], "මම පාසලට යනවා.")

    def test_you_go_to_school(self):
        result = translate_signs(["YOU", "SCHOOL", "GO"])
        self.assertEqual(result["english"], "You are going to school.")

    def test_i_eat_food(self):
        result = translate_signs(["I", "FOOD", "EAT"])
        self.assertEqual(result["english"], "I eat food.")
        self.assertEqual(result["pattern"], "SUBJECT_OBJECT_ACTION")

    def test_you_drink_water(self):
        result = translate_signs(["YOU", "WATER", "DRINK"])
        self.assertEqual(result["english"], "You drink water.")

    def test_unknown_sign(self):
        result = translate_signs(["I", "UNKNOWN", "GO"])
        self.assertEqual(result["pattern"], "UNKNOWN")
        self.assertIsNone(result["english"])
        self.assertIsNone(result["sinhala"])


if __name__ == "__main__":
    unittest.main()
