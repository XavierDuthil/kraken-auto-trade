import logging

import configurations
import utils

logger = logging.getLogger('trader')
logger.addHandler(logging.FileHandler('log/trader.log', 'w'))


class Trader:
    def __init__(self, price_history, ledgers_by_pair):
        self.price_history = price_history
        self.ledgers_by_pair = ledgers_by_pair
        pass

    def auto_trade(self):
        for pair in self.price_history:
            self.auto_trade_pair(pair)
        logger.info('=================================')

    def auto_trade_pair(self, pair):
        prices = self.price_history[pair]
        if len(prices) < 2:
            return

        try:
            differences_by_anteriorities = get_differences_by_anteriorities(prices)
            log_price_evolution(pair, differences_by_anteriorities)

            if should_sell(prices):
                self.sell(pair)
            elif should_buy(prices):
                self.buy(pair)

        except Exception as e:
            logger.exception('auto_trade failed')

    def buy(self, pair):
        last_known_price = self.price_history[pair][-1]
        buy_amount = configurations.base_trade_amount_in_euros / last_known_price
        logger.info(f'Buying {buy_amount:.4f} {pair} at {last_known_price:.2f}€')
        self.ledgers_by_pair[pair].add_buy(buy_amount, configurations.base_trade_amount_in_euros)
        self.ledgers_by_pair[pair].calculate_return(last_known_price)

    def sell(self, pair):
        last_known_price = self.price_history[pair][-1]
        sell_amount = configurations.base_trade_amount_in_euros / last_known_price
        logger.info(f'Selling {sell_amount:.4f} {pair} at {last_known_price:.2f}€')
        self.ledgers_by_pair[pair].add_sell(sell_amount, configurations.base_trade_amount_in_euros)
        self.ledgers_by_pair[pair].calculate_return(last_known_price)


# Sell only if price is going up since 1440/360/60/30min (depending on the risk level)
# and is starting to go down (over 5 min)
def should_sell(prices):
    try:
        current_price = prices[-1]
        if (
            # Ensure that price is starting to go down
            current_price > prices[-5] or
            # Ensure that price is significantly higher than 30 minutes ago
            calculate_difference(prices[-30], current_price) < configurations.minimum_interesting_difference_in_percentage or
            # Ensure that price was increasing since 1440/360/60/30min (depending on the risk level)
            (configurations.trading_risk_level <= 3 and prices[-10] < prices[-30]) or
            (configurations.trading_risk_level <= 2 and prices[-30] < prices[-60]) or
            (configurations.trading_risk_level <= 1 and prices[-60] < prices[-360]) or
            (configurations.trading_risk_level == 0 and prices[-360] < prices[-1440])
        ):
            return False
        return True

    except IndexError:
        return False


# Buy only if price is going down since 1440/360/60/30min (depending on the risk level)
# and is starting to go up
def should_buy(prices):
    try:
        current_price = prices[-1]
        if (
            # Ensure that price is starting to go up
            current_price < prices[-5] or
            # Ensure that price is significantly lower than 30 minutes ago
            calculate_difference(prices[-30], current_price) > -configurations.minimum_interesting_difference_in_percentage or
            # Ensure that price was decreasing since 1440/360/60/30min (depending on the risk level)
            (configurations.trading_risk_level <= 3 and prices[-10] > prices[-30]) or
            (configurations.trading_risk_level <= 2 and prices[-30] > prices[-60]) or
            (configurations.trading_risk_level <= 1 and prices[-60] > prices[-360]) or
            (configurations.trading_risk_level == 0 and prices[-360] > prices[-1440])
        ):
            return False
        return True

    except IndexError:
        return False


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


def log_price_evolution(pair, differences_by_anteriorities):
    diff_message = ''
    for anteriority, difference in differences_by_anteriorities.items():
        # No log if the difference is too small
        # if abs(difference) < configurations.minimum_interesting_difference_in_percentage:
        #     continue

        difference_str = get_printable_difference(difference)
        diff_message += f'\n    Over {anteriority} minute(s): {difference_str}'

    if diff_message:
        logger.info(f'{pair}:')
        for line in diff_message.split('\n')[1:]:
            logger.info(line)


def get_printable_difference(difference):
    return utils.get_colored_value(difference, suffix='%')
