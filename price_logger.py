import logging
from datetime import datetime, timedelta

from configurations import price_logging_period_in_minutes


class PriceLogger:
    next_log_time = datetime.now()

    def __init__(self, price_history):
        self.price_history = price_history

    def log_price(self):
        if not self.price_history or datetime.now() < self.next_log_time:
            return

        last_prices = self.price_history[-1]
        logging.info(f'Prices: {last_prices}')

        self.next_log_time = self.next_log_time + timedelta(minutes=price_logging_period_in_minutes)
