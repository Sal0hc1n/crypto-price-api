from exchanges.tools.base import Exchange

class Poloniex(Exchange):
    name = 'polinex'
    TICKER_URL = 'https://poloniex.com/public?command=returnTicker'
    UNDERLYING_DICT = {
        'BTCUSDT' : 'USDT_BTC',
        'ETHBTC' : 'BTC_ETH',
        'XRPBTC' : 'BTC_XRP',
        'LTCBTC' : 'BTC_LTC',
        'DASHBTC' : 'BTC_DASH',
        'BTHBTC' : 'BTC_BCH',
        'XMRBTC' : 'BTC_XMR',
        'ZECBTC' : 'BTC_ZEC',
        'SCBTC' : 'BTC_SC'
    }
    QUOTE_DICT = {
        'bid' : 'highestBid',
        'ask' : 'lowestAsk',
        'last' : 'last'
    }

    @classmethod
    def _quote_extractor(cls, data, underlying, quote):
        return data.get(cls.UNDERLYING_DICT[underlying]).get(cls.QUOTE_DICT[quote])
