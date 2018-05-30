from exchanges.tools.base import Exchange

class Cex(Exchange):

    TICKER_URL = 'https://cex.io/api/ticker/%s'
    UNDERLYING_DICT = {
        'BTCUSD' : 'BTC/USD',
        'BTCEUR' : 'BTC/EUR'
    }

    @classmethod
    def _quote_extractor(cls, data, underlying, quote):
        return data.get(cls.QUOTE_DICT[quote])

    @classmethod
    def _current_price_extractor(cls, data, underlying):
        return data.get('last')

    @classmethod
    def _current_bid_extractor(cls, data, underlying):
        return data.get('bid')

    @classmethod
    def _current_ask_extractor(cls, data, underlying):
        return data.get('ask')
