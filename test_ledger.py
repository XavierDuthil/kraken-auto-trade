from unittest import TestCase

import configurations
import ledger


class Case:
    def __init__(self, name, args=None, expected=None):
        self.name = name
        self.args = args
        self.expected = expected


class TestLedger(TestCase):
    configurations.fee_percentage = 0

    def test_calculate_return(self):
        test_cases = [
            Case(
                name='Only good buys',
                args={
                    'last_known_price': 100,
                    'operations': [
                        ledger.Operation('BCHEUR', 1, 90, ledger.Buy),
                        ledger.Operation('BCHEUR', 1, 95, ledger.Buy),
                        ledger.Operation('BCHEUR', 1, 100, ledger.Buy),
                    ],
                },
                expected=15,
            ),
            Case(
                name='Good and bad buys',
                args={
                    'last_known_price': 100,
                    'operations': [
                        ledger.Operation('BCHEUR', 1, 90, ledger.Buy),
                        ledger.Operation('BCHEUR', 1, 110, ledger.Buy),
                        ledger.Operation('BCHEUR', 1, 100, ledger.Buy),
                    ],
                },
                expected=0,
            ),
            Case(
                name='Only bad buys',
                args={
                    'last_known_price': 100,
                    'operations': [
                        ledger.Operation('BCHEUR', 1, 115, ledger.Buy),
                        ledger.Operation('BCHEUR', 0.5, 55, ledger.Buy),
                    ],
                },
                expected=-20,
            ),
            Case(
                name='Only good sells',
                args={
                    'last_known_price': 100,
                    'operations': [
                        ledger.Operation('BCHEUR', 1, 115, ledger.Sell),
                        ledger.Operation('BCHEUR', 1, 110, ledger.Sell),
                        ledger.Operation('BCHEUR', 1, 100, ledger.Sell),
                    ],
                },
                expected=25,
            ),
            Case(
                name='Only bad sells',
                args={
                    'last_known_price': 100,
                    'operations': [
                        ledger.Operation('BCHEUR', 1, 80, ledger.Sell),
                        ledger.Operation('BCHEUR', 0.5, 45, ledger.Sell),
                        ledger.Operation('BCHEUR', 1, 100, ledger.Sell),
                    ],
                },
                expected=-25,
            ),
        ]

        for test_case in test_cases:
            test_ledger = ledger.Ledger('BCHEUR')
            test_ledger.operations = test_case.args['operations']

            got = test_ledger.calculate_return(test_case.args['last_known_price'])
            self.assertEqual(got, test_case.expected, test_case.name)
