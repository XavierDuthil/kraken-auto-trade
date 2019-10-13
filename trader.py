import logging

import configurations
import utils


class Trader:
    def __init__(self, price_history, ledgers_by_pair):
        self.price_history = price_history
        self.ledgers_by_pair = ledgers_by_pair
        pass

    def auto_trade(self):
        for pair in self.price_history:
            self.auto_trade_pair(pair)
        logging.info('=================================')

    def auto_trade_pair(self, pair):
        prices = self.price_history[pair]
        if len(prices) < 2:
            return

        diff_message = ''
        for anteriority, difference in get_differences_by_anteriorities(prices).items():
            # Ignore if the difference is too little
            if abs(difference) < configurations.minimum_interesting_difference_in_percentage:
                continue

            difference_str = get_printable_difference(difference)
            diff_message += f'\n    Over {anteriority} minute(s): {difference_str}'

            # Trade only if difference is over an anteriority of 10 minutes
            if anteriority != 10:
                continue
            if difference > 0:
                self.sell(pair)
            else:
                self.buy(pair)

        if diff_message:
            logging.info(f'{pair}:')
            for line in diff_message.split('\n')[1:]:
                logging.info(line)

    def buy(self, pair):
        last_known_price = self.price_history[pair][-1]
        buy_amount = configurations.base_trade_amount_in_euros / last_known_price
        logging.info(f'Buying {buy_amount} {pair} at {last_known_price}')
        self.ledgers_by_pair[pair].add_buy(buy_amount, configurations.base_trade_amount_in_euros)
        self.ledgers_by_pair[pair].calculate_return(last_known_price)

    def sell(self, pair):
        last_known_price = self.price_history[pair][-1]
        sell_amount = configurations.base_trade_amount_in_euros / last_known_price
        logging.info(f'Selling {sell_amount} {pair} at {last_known_price}')
        self.ledgers_by_pair[pair].add_sell(sell_amount, configurations.base_trade_amount_in_euros)
        self.ledgers_by_pair[pair].calculate_return(last_known_price)


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
    return utils.get_colored_value(difference, suffix='%')
