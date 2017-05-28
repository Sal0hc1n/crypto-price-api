from exchanges.base import Exchange

class HitBTC(Exchange):

    TICKER_URL = 'https://api.hitbtc.com/api/1/public/%s/ticker'
    SUPPORTED_UNDERLYINGS = ['BTCUSD', 'BTCEUR', 'ETHBTC']
    UNDERLYING_DICT = {
        'BTCUSD' : 'BTCUSD',
        'BTCEUR' : 'BTCEUR',
        'ETHBTC' : 'ETHBTC'
    }

    @classmethod
    def _quote_extractor(cls, data, underlying, quote):
        return data.get(cls.QUOTE_DICT[quote])
