
import unittest

from src.translation.topk_context_selector import select_candidate


def make_sequence(first_candidates, second, third):
    return [
        {
            "top_k": [
                {"gloss": gloss, "score": score}
                for gloss, score in first_candidates
            ]
        },
        {"top_k": [{"gloss": second, "score": 0.95}]},
        {"top_k": [{"gloss": third, "score": 0.94}]}
    ]


class TestGeneralizedContext(unittest.TestCase):

    def test_subject_with_home(self):
        sequence = make_sequence(
            [("ME", 0.90), ("I", 0.75)],
            "HOME",
            "GO"
        )

        result = select_candidate(sequence, 0)

        self.assertEqual(result["selected"], "I")

    def test_subject_with_eating(self):
        sequence = make_sequence(
            [("ME", 0.88), ("I", 0.72)],
            "FOOD",
            "EAT"
        )

        result = select_candidate(sequence, 0)

        self.assertEqual(result["selected"], "I")

    def test_possessive_not_selected_as_subject(self):
        sequence = make_sequence(
            [("MINE", 0.91), ("I", 0.70)],
            "GO",
            "SCHOOL"
        )

        result = select_candidate(sequence, 0)

        self.assertEqual(result["selected"], "I")

    def test_no_context_stays_ambiguous(self):
        sequence = [
            {
                "top_k": [
                    {"gloss": "ME", "score": 0.90},
                    {"gloss": "I", "score": 0.75}
                ]
            },
            {
                "top_k": [
                    {"gloss": "WATER", "score": 0.95}
                ]
            }
        ]

        result = select_candidate(sequence, 0)

        self.assertEqual(result["status"], "AMBIGUOUS")

    def test_month_context(self):
        sequence = [
            {"top_k": [{"gloss": "MONTH", "score": 0.9}]},
            {
                "top_k": [
                    {"gloss": "FRIEND", "score": 0.85},
                    {"gloss": "FRIDAY", "score": 0.80},
                    {"gloss": "FEBRUARY", "score": 0.70}
                ]
            }
        ]

        result = select_candidate(sequence, 1)

        self.assertEqual(result["status"], "RESOLVED")
        self.assertEqual(result["selected"], "FEBRUARY")


if __name__ == "__main__":
    unittest.main()
