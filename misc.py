import krakenex
from pykrakenapi import KrakenAPI
from currency_viewer import currency_viewer as cv

# # Tests with pykrakenapi
# api = krakenex.API()
# k = KrakenAPI(api)
#
# for row in k.get_tradable_asset_pairs().iterrows():
#     print(row)

# ohlc, last = k.get_ohlc_data("ETHUSD")
# print(ohlc)
# data, last = k.get_recent_spread_data("ETHUSD")
# print(data)
# data, last = k.get_recent_trades("ETHUSD")
# print(last)
# print(k.get_ticker_information("ETHUSD"))
# print(k.get_tradable_asset_pairs())
# help(KrakenAPI)

# # Tests with CurrencyViewer
# a = cv.CurrencyViewer()
# print(a.extract_market_data())
# a.processCViewer(log=True, currency="USD", time="rfc1123")
