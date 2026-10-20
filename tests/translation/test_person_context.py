import unittest

from src.translation.topk_context_selector import select_candidate


class TestPersonContext(unittest.TestCase):

    def test_person_context_overrides_higher_score(self):
        sequence = [
            {"top_k": [{"gloss": "I", "score": 0.95}]},
            {"top_k": [{"gloss": "SEE", "score": 0.93}]},
            {
                "top_k": [
                    {"gloss": "FRIDAY", "score": 0.88},
                    {"gloss": "FRIEND", "score": 0.75},
                    {"gloss": "FEBRUARY", "score": 0.65}
                ]
            }
        ]

        result = select_candidate(sequence, 2)

        self.assertEqual(result["status"], "RESOLVED")
        self.assertEqual(result["selected"], "FRIEND")
        self.assertEqual(
            result["recognition_baseline"], "FRIDAY"
        )


if __name__ == "__main__":
    unittest.main()