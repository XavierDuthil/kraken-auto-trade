import logging

import coloredlogs

import configurations


class Trader:
    def __init__(self):
        pass

    def trade(self, price_history):
        if len(price_history) < 2:
            return

        for pair, last_price in price_history[-1].items():
            logging.info(f'{pair}:')
            for anteriority in configurations.anteriorities_in_minutes:
                # Stop if history doesn't go that far
                if len(price_history) < anteriority:
                    continue

                old_price = price_history[-anteriority][pair]
                difference = calculate_difference(old_price, last_price)
                difference_str = get_printable_difference(difference)
                logging.info(f'    Over {anteriority} minute(s): {difference_str}')


def calculate_difference(old_price, new_price):
    if old_price == new_price:
        return 0
    return (new_price - old_price) * 100 / old_price


def get_printable_difference(difference):
    difference_str = f'{difference:.02f}%'
    if difference >= 0.005:
        return coloredlogs.ansi_wrap('+' + difference_str, color='green')
    elif difference <= -0.005:
        return coloredlogs.ansi_wrap(difference_str, color='red')
    return difference_str
