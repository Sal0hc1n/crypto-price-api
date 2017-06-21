from exchanges.base import Exchange

class Gemini(Exchange):

    TICKER_URL = 'https://api.gemini.com/v1/pubticker/%s'
    UNDERLYING_DICT = {
        'BTCUSD' : 'btcusd',
        'ETHUSD' : 'ethusd',
        'ETHBTC' : 'ethbtc'
    }

    @classmethod
    def _quote_extractor(cls, data, underlying, quote):
        return data.get(cls.QUOTE_DICT[quote])
