from exchanges.base import Exchange


class Bitfinex(Exchange):

    TICKER_URL = 'https://api.bitfinex.com/v1/pubticker/%s'
    UNDERLYING_DICT = {
        'BTCUSD' : 'btcusd',
        'ETHBTC' : 'ethbtc',
        'XRPBTC' : 'xrpbtc'
    }
    QUOTE_DICT = {
        'last' : 'last_price',
        'bid' : 'bid',
        'ask' : 'ask'
    }

    @classmethod
    def _quote_extractor(cls, data, underlying, quote):
        return data.get(cls.QUOTE_DICT[quote])

    @classmethod
    def _last_price_extractor(cls, data, underlying):
        return data.get('last_price')

    @classmethod
    def _current_bid_extractor(cls, data, underlying):
        return data.get('bid')

    @classmethod
    def _current_ask_extractor(cls, data, underlying):
        return data.get('ask')
