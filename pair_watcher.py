import time
from collections import defaultdict

import configurations


class PairWatcher:
    price_history = []

    def __init__(self, pairs, api):
        if not pairs:
            raise ValueError("invalid argument: pairs cannot be empty")
        self.pairs = pairs
        self.pairs_str = ','.join(pairs)
        self.api = api

    def watch(self):
        price_by_pair = self.get_market_averaged_price(configurations.averaged_price_time_span_in_seconds)
        self.price_history.append(price_by_pair)
        self.price_history = self.price_history[:configurations.maximum_elements_in_price_history]

    def get_market_averaged_price(self, time_span_in_seconds):
        last_prices_by_pair = defaultdict(list)
        end_of_minute = time.time() + time_span_in_seconds
        while time.time() < end_of_minute:
            for pair, price in self.get_market_price().items():
                last_prices_by_pair[pair].append(price)
            time.sleep(configurations.ticker_delay_in_seconds)

        return get_average_price_by_pair(last_prices_by_pair)

    def get_market_price(self):
        data = self.api.query_public('Ticker', {'pair': self.pairs_str})
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
