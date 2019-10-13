import logging
from datetime import datetime

import configurations
import utils

Buy, Sell = range(0, 2)


class Operation:
    def __init__(self, pair, amount, price, kind):
        self.date = datetime.now()
        self.pair = pair
        self.theoretical_price = price
        self.amount = amount
        self.kind = kind
        self.fee = price * configurations.fee_percentage / 100

        if kind == Buy:
            self.real_price = price + self.fee
        else:
            self.real_price = price - self.fee


class Ledger:
    def __init__(self, pair):
        self.operations = []
        self.pair = pair
        self.initial_fiat_amount = 0
        self.initial_crypto_amount = 0

    def add_buy(self, amount, price):
        new_operation = Operation(self.pair, amount, price, Buy)
        self.operations.append(new_operation)

    def add_sell(self, amount, price):
        new_operation = Operation(self.pair, amount, price, Sell)
        self.operations.append(new_operation)

    def calculate_return(self, last_known_price):
        crypto_diff = 0
        fiat_diff = 0
        total_fees = 0

        for operation in self.operations:
            total_fees += operation.fee
            if operation.kind == Buy:
                crypto_diff += operation.amount
                fiat_diff -= operation.real_price
            else:
                crypto_diff -= operation.amount
                fiat_diff += operation.real_price

        total_return = crypto_diff * last_known_price + fiat_diff
        logging.info(f'{self.pair} crypto diff: {utils.get_colored_value(crypto_diff)}')
        logging.info(f'{self.pair} fiat diff: {utils.get_colored_value(fiat_diff, suffix="€")}')
        logging.info(f'{self.pair} total fees: {total_fees}€')
        logging.info(f'{self.pair} => total return: {utils.get_colored_value(total_return, suffix="€")}')
        return total_return
