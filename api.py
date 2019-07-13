import krakenex
from pykrakenapi import KrakenAPI
from time import sleep
from currency_viewer import currency_viewer as cv

api = krakenex.API()

def get_market_price(pair):
    data = api.query_public('Ticker', {'pair': pair})
    first_key = list(data['result'])[0] # api-side string representation of the given pair
    return data['result'][first_key]['c'][0] # 'c' represents the last trade's value

# # Tests with pykrakenapi
# k = KrakenAPI(api)
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

if __name__ == "__main__":
    while True:
        price = get_market_price("ETHUSD")
        print(price)
        sleep(0.5)
