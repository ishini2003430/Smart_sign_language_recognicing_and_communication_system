
import unittest

from src.translation.app import translate_signs


class TestFamilyGrammar(unittest.TestCase):

    def test_mother_comes_home(self):
        result = translate_signs(
            ["MOTHER", "HOME", "COME"]
        )

        self.assertEqual(
            result["english"],
            "Mother is coming home."
        )

        self.assertEqual(
            result["sinhala"],
            "අම්මා ගෙදර එනවා."
        )

    def test_father_goes_school(self):
        result = translate_signs(
            ["FATHER", "SCHOOL", "GO"]
        )

        self.assertEqual(
            result["english"],
            "Father is going to school."
        )

    def test_sister_goes_home(self):
        result = translate_signs(
            ["SISTER", "HOME", "GO"]
        )

        self.assertEqual(
            result["sinhala"],
            "සහෝදරිය ගෙදර යනවා."
        )

    def test_brother_comes_school(self):
        result = translate_signs(
            ["BROTHER", "SCHOOL", "COME"]
        )

        self.assertEqual(
            result["english"],
            "Brother is coming to school."
        )

    def test_alternative_order(self):
        result = translate_signs(
            ["MOTHER", "COME", "HOME"]
        )

        self.assertEqual(
            result["english"],
            "Mother is coming home."
        )

    def test_unsupported_person_action(self):
        result = translate_signs(
            ["MOTHER", "SCHOOL", "EAT"]
        )

        self.assertEqual(result["pattern"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
