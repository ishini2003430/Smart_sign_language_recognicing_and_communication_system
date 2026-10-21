
import unittest

from src.translation.app import translate_signs


class TestPersonActions(unittest.TestCase):

    def test_see_father(self):
        result = translate_signs(
            ["I", "FATHER", "SEE"]
        )

        self.assertEqual(
            result["english"],
            "I see a father."
        )
        self.assertEqual(
            result["sinhala"],
            "මම තාත්තාව දකිනවා."
        )

    def test_see_mother_alternative_order(self):
        result = translate_signs(
            ["YOU", "SEE", "MOTHER"]
        )

        self.assertEqual(
            result["english"],
            "You see a mother."
        )
        self.assertEqual(
            result["sinhala"],
            "ඔයා අම්මාව දකිනවා."
        )

    def test_know_friend(self):
        result = translate_signs(
            ["I", "FRIEND", "KNOW"]
        )

        self.assertEqual(
            result["english"],
            "I know a friend."
        )
        self.assertEqual(
            result["sinhala"],
            "මම මිතුරාව දන්නවා."
        )

    def test_know_brother(self):
        result = translate_signs(
            ["YOU", "KNOW", "BROTHER"]
        )

        self.assertEqual(
            result["english"],
            "You know a brother."
        )

    def test_unsupported_relation(self):
        result = translate_signs(
            ["I", "SCHOOL", "KNOW"]
        )

        self.assertEqual(
            result["pattern"],
            "UNKNOWN"
        )


if __name__ == "__main__":
    unittest.main()
