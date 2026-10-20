
import unittest

from src.translation.context_disambiguation import disambiguate_sign


class TestContextDisambiguation(unittest.TestCase):

    def test_person_context(self):
        result = disambiguate_sign("SIGN_FORM_G01", "PERSON")

        self.assertEqual(result["status"], "RESOLVED")
        self.assertEqual(
            result["selected_meaning"]["gloss"],
            "FRIEND"
        )

    def test_weekday_context(self):
        result = disambiguate_sign("SIGN_FORM_G01", "WEEKDAY")

        self.assertEqual(result["status"], "RESOLVED")
        self.assertEqual(
            result["selected_meaning"]["gloss"],
            "FRIDAY"
        )

    def test_month_context(self):
        result = disambiguate_sign("SIGN_FORM_G01", "MONTH")

        self.assertEqual(result["status"], "RESOLVED")
        self.assertEqual(
            result["selected_meaning"]["gloss"],
            "FEBRUARY"
        )

    def test_missing_context(self):
        result = disambiguate_sign("SIGN_FORM_G01")

        self.assertEqual(result["status"], "AMBIGUOUS")
        self.assertIsNone(result["selected_meaning"])

    def test_unknown_sign_form(self):
        result = disambiguate_sign("UNKNOWN_FORM", "PERSON")

        self.assertEqual(result["status"], "UNKNOWN_SIGN_FORM")
        self.assertIsNone(result["selected_meaning"])


if __name__ == "__main__":
    unittest.main()
