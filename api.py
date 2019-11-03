import logging
import sys

import coloredlogs
import krakenex

from configurations import pairs_to_watch
from ledger import Ledger
from pair_watcher import PairWatcher
from price_logger import PriceLogger
from trader import Trader

asctime_colored = coloredlogs.ansi_wrap('%(asctime)-19s', color='green')
name_colored = coloredlogs.ansi_wrap('%(name)-7s', color='blue')
levelname_colored = coloredlogs.ansi_wrap('%(levelname)-8s', color='black')

logging._defaultFormatter = logging.Formatter(
    fmt=f'{asctime_colored} {name_colored} {levelname_colored} %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logging.basicConfig(
    level=logging.INFO,
    format=f'{asctime_colored} {name_colored} {levelname_colored} %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler('log/main.log', 'w')]
)


if __name__ == '__main__':
    logging.info('Initializing')
    logging.info(f'Pairs to watch: {pairs_to_watch}')

    ledgers_by_pair = {}
    for pair in pairs_to_watch:
        ledgers_by_pair[pair] = Ledger(pair)

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
