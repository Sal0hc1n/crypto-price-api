from exchanges.base import Exchange

class CexIO(Exchange):

    TICKER_URL = 'https://cex.io/api/ticker/%s'
    SUPPORTED_UNDERLYINGS = ['BTCUSD', 'BTCEUR']
    UNDERLYING_DICT = {
        'BTCUSD' : 'BTC/USD',
        'BTCEUR' : 'BTC/EUR'
    }

    @classmethod
    def _quote_extractor(cls, data, underlying, quote):
        return data.get(cls.QUOTE_DICT[quote])
