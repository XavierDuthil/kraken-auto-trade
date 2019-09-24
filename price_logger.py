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

        log_message = ''

        for pair, prices in self.price_history.items():
            last_price = prices[-1]
            if last_price >= 10:
                log_message += pair + f': {last_price:.2f}, '
            else:
                log_message += pair + f': {last_price:.4f}, '

        log_message = log_message[:-2]
        logging.info(log_message)

        self.next_log_time = self.next_log_time + timedelta(minutes=price_logging_period_in_minutes)
