import logging
import time
import sys
from collections import defaultdict
import coloredlogs
import krakenex

api = krakenex.API()

coloredlogs.install(
    fmt='%(asctime)s %(levelname)s %(message)s',
    stream=sys.stdout,
    level=logging.INFO,
)

ticker_delay_in_seconds = 1
averaged_price_time_span_in_seconds = 60
anteriorities_in_minutes = [1, 5, 10, 15, 30, 60, 180, 360, 1440]
pairs_to_watch = ['XXBTZEUR', 'XETHZEUR', 'XXMRZEUR', 'XLTCZEUR', 'XXRPZEUR', 'DASHEUR', 'BCHEUR']


class PairWatcher:
    price_history = []

    def __init__(self, pairs):
        if not pairs:
            raise ValueError("invalid argument: pairs cannot be empty")
        self.pairs = pairs
        self.pairs_str = ','.join(pairs)

    def watch(self, time_span_in_seconds):
        price_by_pair = self.get_market_averaged_price(time_span_in_seconds)

        for pair, price in price_by_pair.items():
            logging.info(f'{pair}:')
            for anteriority in anteriorities_in_minutes:
                # Stop if history doesn't go that far
                if len(self.price_history) < anteriority:
                    continue

                old_price = self.price_history[-anteriority][pair]
                new_price = price_by_pair[pair]
                difference_str = get_printable_difference(old_price, new_price)
                logging.info(f'    Over {anteriority} minute(s): {difference_str}')

        self.price_history.append(price_by_pair)

    def get_market_averaged_price(self, time_span_in_seconds):
        last_prices_by_pair = defaultdict(list)
        end_of_minute = time.time() + time_span_in_seconds
        while time.time() < end_of_minute:
            for pair, price in self.get_market_price().items():
                last_prices_by_pair[pair].append(price)
            time.sleep(ticker_delay_in_seconds)

        return get_average_price_by_pair(last_prices_by_pair)

    def get_market_price(self):
        data = api.query_public('Ticker', {'pair': self.pairs_str})
        last_price_by_pair = {}
        for key, value in data['result'].items():
            last_price_by_pair[key] = float(value['c'][0])
        return last_price_by_pair


def get_average_price_by_pair(last_prices_by_pair):
    averaged_price_by_pair = {}
    for pair, prices in last_prices_by_pair.items():
        last_prices = last_prices_by_pair[pair]
        averaged_price_by_pair[pair] = sum(last_prices) / len(last_prices)
    return averaged_price_by_pair


def get_printable_difference(old_price, new_price):
    difference = calculate_difference(old_price, new_price)
    difference_str = f'{difference:.02f}%'
    if difference > 0:
        return coloredlogs.ansi_wrap('+' + difference_str, color='green')
    elif difference < 0:
        return coloredlogs.ansi_wrap(difference_str, color='red')
    return difference_str


def calculate_difference(old_price, new_price):
    if old_price == new_price:
        return 0
    return (new_price - old_price) * 100 / old_price


if __name__ == '__main__':
    logging.info('Initializing')
    pair_watcher = PairWatcher(pairs_to_watch)

    previous_price_by_pair = {}
    while True:
        pair_watcher.watch(averaged_price_time_span_in_seconds)
        # logging.info(pair_watcher.get_market_price())

        # price_by_pair = pair_watcher.get_market_averaged_price(averaged_price_time_span_in_seconds)
        # logging.info(price_by_pair)
        #
        # for pair, price in price_by_pair.items():
        #     if pair not in previous_price_by_pair:
        #         continue
        #
        #     difference = calculate_difference(previous_price_by_pair[pair], price_by_pair[pair])
        #     print('{}: {:.2f}%'.format(pair, difference))
        #
        # previous_price_by_pair = price_by_pair
