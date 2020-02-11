from unittest import TestCase

import configurations
import pair_watcher


class Case:
    def __init__(self, name, args=None, expected=None):
        self.name = name
        self.args = args
        self.expected = expected


class TestPairWatcher(TestCase):
    configurations.maximum_elements_in_price_history = 4

    def test_add_to_price_history(self):
        test_cases = [
            Case(
                name='Check that history rotates correctly when max elements is reached',
                args={
                    'last_prices_by_pair': [
                        {"BCHEUR": 1},
                        {"BCHEUR": 2},
                        {"BCHEUR": 3},
                        {"BCHEUR": 4},
                        {"BCHEUR": 5},
                        {"BCHEUR": 6},
                        {"BCHEUR": 7},
                        {"BCHEUR": 8},
                        {"BCHEUR": 9},
                    ],
                },
                expected={
                    "BCHEUR": [5, 6, 7, 8, 9]
                },
            ),
        ]

        for test_case in test_cases:
            test_pair_watcher = pair_watcher.PairWatcher(['BCHEUR'], None)
            for last_price_by_pair in test_case.args["last_prices_by_pair"]:
                test_pair_watcher.add_to_price_history(last_price_by_pair)

            self.assertEqual(test_pair_watcher.price_history, test_case.expected, test_case.name)
