from exchanges.tools.base import Exchange

class BitFlyer(Exchange):

    name = 'bitflyer'
    TICKER_URL = 'https://api.bitflyer.jp/v1/ticker/?product_code=%s'
    UNDERLYING_DICT = {
        'ETHBTC' : 'ETH_BTC',
        'BTCJPY' : 'BTC_JPY'
    }

    QUOTE_DICT = {
        'bid' : 'best_bid',
        'ask' : 'best_ask',
        'last' : 'ltp'
    }

    @classmethod
    def _quote_extractor(cls, data, underlying, quote):
        return data.get(cls.QUOTE_DICT[quote])
