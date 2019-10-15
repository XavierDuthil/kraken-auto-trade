import logging
import sys

import coloredlogs
import krakenex

import ledger
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
    logging.info(f'Pairs to watch: {pairs_to_watch}')

    ledgers_by_pair = {}
    for pair in pairs_to_watch:
        ledgers_by_pair[pair] = ledger.Ledger(pair)

    api = krakenex.API()
    pair_watcher = PairWatcher(pairs_to_watch, api)
    price_logger = PriceLogger(pair_watcher.price_history)
    trader = Trader(pair_watcher.price_history, ledgers_by_pair)

    logging.info(f'Fetching price history')
    pair_watcher.get_price_history()

    logging.info(f'Starting watch')
    while True:
        try:
            price_logger.log_price()
            trader.auto_trade()
            pair_watcher.watch()
        except Exception as e:
            logging.error(f'main: an error occurred: {e}')
