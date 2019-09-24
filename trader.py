import logging

import coloredlogs

import configurations


class Trader:
    def __init__(self, price_history):
        self.price_history = price_history
        pass

    def auto_trade(self):
        for pair in self.price_history:
            self.auto_trade_pair(pair)

    def auto_trade_pair(self, pair):
        prices = self.price_history[pair]
        if len(prices) < 2:
            return

        diff_message = ''
        for anteriority, difference in get_differences_by_anteriorities(prices).items():
            difference_str = get_printable_difference(difference)
            diff_message += f'\n    Over {anteriority} minute(s): {difference_str}'

        if diff_message:
            logging.info(f'{pair}:')
            for line in diff_message.split('\n')[1:]:
                logging.info(line)


def get_differences_by_anteriorities(prices):
    differences_by_anteriorities = {}
    last_price = prices[-1]
    for anteriority in configurations.anteriorities_in_minutes:
        # Stop if history doesn't go that far
        if len(prices) < anteriority + 1:
            continue

        old_price = prices[-anteriority - 1]
        differences_by_anteriorities[anteriority] = calculate_difference(old_price, last_price)

    return differences_by_anteriorities


def calculate_difference(old_price, new_price):
    if old_price == new_price:
        return 0
    return (new_price - old_price) * 100 / old_price


def get_printable_difference(difference):
    difference_str = f'{+difference:.02f}%'
    if difference >= 0.005:
        return coloredlogs.ansi_wrap(difference_str, color='green')
    elif difference <= -0.005:
        return coloredlogs.ansi_wrap(difference_str, color='red')
    return difference_str
