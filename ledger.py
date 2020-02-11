import logging
from datetime import datetime

import configurations
import utils

Buy, Sell = range(0, 2)

logger = logging.getLogger('ledger')
logger.addHandler(logging.FileHandler('log/ledger.log', 'w'))

wallet_euros = 200


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
        self.current_amount = 0

        # Amounts to ~25€ for each currency
        if pair == "XXBTZEUR":
            self.current_amount = 0.0028
        elif pair == "XETHZEUR":
            self.current_amount = 0.12
        elif pair == "XXMRZEUR":
            self.current_amount = 0.325
        elif pair == "XLTCZEUR":
            self.current_amount = 0.37
        elif pair == "XXRPZEUR":
            self.current_amount = 100
        elif pair == "DASHEUR":
            self.current_amount = 0.22
        elif pair == "BCHEUR":
            self.current_amount = 0.06

    def add_buy(self, amount, price):
        global wallet_euros
        new_operation = Operation(self.pair, amount, price, Buy)

        if wallet_euros - new_operation.real_price < 0:
            logger.warning(f"Can't buy {new_operation.amount:.4f} {self.pair}: not enough euros ({wallet_euros:.2f}€)")
            return

        wallet_euros -= new_operation.real_price
        self.current_amount += new_operation.amount
        logger.info(f"{wallet_euros:.2f}€ in wallet")
        self.operations.append(new_operation)

    def add_sell(self, amount, price):
        global wallet_euros
        new_operation = Operation(self.pair, amount, price, Sell)

        if self.current_amount - new_operation.amount < 0:
            logger.warning(f"Can't sell {new_operation.amount} {self.pair}: not enough tokens ({self.current_amount:.4f} {self.pair})")
            return

        wallet_euros += new_operation.real_price
        self.current_amount -= new_operation.amount
        logger.info(f"{wallet_euros:.2f}€ in wallet")
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
        logger.info(f'{self.pair} crypto diff: {utils.get_colored_value(crypto_diff)}')
        logger.info(f'{self.pair} fiat diff: {utils.get_colored_value(fiat_diff, suffix="€")}')
        logger.info(f'{self.pair} total fees: {total_fees:.2f}€')
        logger.info(f'{self.pair} => total return: {utils.get_colored_value(total_return, suffix="€")}')
        return total_return
