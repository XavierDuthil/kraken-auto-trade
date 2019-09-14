import logging
import sys

import coloredlogs
import krakenex

from configurations import pairs_to_watch
from pair_watcher import PairWatcher
from price_logger import PriceLogger
from trader import Trader

coloredlogs.install(
    fmt='%(asctime)s %(levelname)s %(message)s',
    stream=sys.stdout,
    level=logging.INFO,
)

if __name__ == '__main__':
    logging.info('Initializing')

    api = krakenex.API()
    pair_watcher = PairWatcher(pairs_to_watch, api)
    price_logger = PriceLogger(pair_watcher.price_history)
    trader = Trader()

    logging.info(f'Starting watch for pairs {pairs_to_watch}')
    while True:
        pair_watcher.watch()
        price_logger.log_price()
        trader.trade(pair_watcher.price_history)
