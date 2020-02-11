from unittest import TestCase

import configurations
import trader


class Case:
    def __init__(self, name, args=None, expected=None):
        self.name = name
        self.args = args
        self.expected = expected


class TestTrader(TestCase):
    def test_get_differences_by_anteriorities(self):
        prices_increasing_then_decreasing_at_the_end = [1] * 1441
        prices_increasing_then_decreasing_at_the_end[-1441] = 100
        prices_increasing_then_decreasing_at_the_end[-361] = 125
        prices_increasing_then_decreasing_at_the_end[-181] = 160
        prices_increasing_then_decreasing_at_the_end[-61] = 200
        prices_increasing_then_decreasing_at_the_end[-31] = 250
        prices_increasing_then_decreasing_at_the_end[-16] = 250
        prices_increasing_then_decreasing_at_the_end[-11] = 400
        prices_increasing_then_decreasing_at_the_end[-6] = 250
        prices_increasing_then_decreasing_at_the_end[-2] = 200
        prices_increasing_then_decreasing_at_the_end[-1] = 200

        test_cases = [
            Case(
                name='Basic test',
                args={
                    'prices': prices_increasing_then_decreasing_at_the_end,
                },
                expected={
                    1: 0,
                    5: -20.0,
                    10: -50.0,
                    15: -20.0,
                    30: -20.0,
                    60: 0,
                    180: 25.0,
                    360: 60.0,
                    1440: 100.0,
                }
            ),
        ]

        for test_case in test_cases:
            got = trader.get_differences_by_anteriorities(test_case.args['prices'])
            self.assertEqual(got, test_case.expected, test_case.name)

    def test_should_sell(self):
        prices_increasing_then_decreasing_at_the_end = [100] * 1441
        prices_increasing_then_decreasing_at_the_end[-1440] = 100
        prices_increasing_then_decreasing_at_the_end[-360] = 125
        prices_increasing_then_decreasing_at_the_end[-60] = 150
        prices_increasing_then_decreasing_at_the_end[-30] = 200
        prices_increasing_then_decreasing_at_the_end[-10] = 250
        prices_increasing_then_decreasing_at_the_end[-5] = 300
        prices_increasing_then_decreasing_at_the_end[-1] = 250

        prices_increasing_except_1440_then_decreasing_at_the_end = prices_increasing_then_decreasing_at_the_end*1  # Makes a copy
        prices_increasing_except_1440_then_decreasing_at_the_end[-1440] = 150

        prices_increasing_then_decreasing_at_the_end_short = [100] * 31
        prices_increasing_then_decreasing_at_the_end_short[-30] = 200
        prices_increasing_then_decreasing_at_the_end_short[-10] = 250
        prices_increasing_then_decreasing_at_the_end_short[-5] = 300
        prices_increasing_then_decreasing_at_the_end_short[-1] = 250

        prices_increasing_short = prices_increasing_then_decreasing_at_the_end_short*1  # Makes a copy
        prices_increasing_short[-1] = 301

        test_cases = [
            Case(
                name='Sell with risk 0',
                args={
                    'risk_level': 0,
                    'prices': prices_increasing_then_decreasing_at_the_end,
                },
                expected=True,
            ),
            Case(
                name="Don't sell with risk 0 because of index -1440",
                args={
                    'risk_level': 0,
                    'prices': prices_increasing_except_1440_then_decreasing_at_the_end,
                },
                expected=False,
            ),
            Case(
                name='Sell with risk 1, ignoring index -1440',
                args={
                    'risk_level': 1,
                    'prices': prices_increasing_except_1440_then_decreasing_at_the_end,
                },
                expected=True,
            ),
            Case(
                name='Sell with risk 3, ignoring indexes > 30',
                args={
                    'risk_level': 3,
                    'prices': prices_increasing_then_decreasing_at_the_end_short,
                },
                expected=True,
            ),
            Case(
                name="Don's sell with risk 3, because price is not going down",
                args={
                    'risk_level': 3,
                    'prices': prices_increasing_short,
                },
                expected=False,
            ),
        ]

        for test_case in test_cases:
            configurations.trading_risk_level = test_case.args['risk_level']
            got = trader.should_sell(test_case.args['prices'])
            self.assertEqual(got, test_case.expected, test_case.name)
