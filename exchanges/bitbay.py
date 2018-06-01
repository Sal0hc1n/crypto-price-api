from exchanges.tools.base import Exchange

class BitBay(Exchange):
    name = 'bitbay'
    TICKER_URL = 'https://bitbay.net/API/Public/%s/ticker.json'
    UNDERLYING_DICT = {
        'BTCUSD' : 'BTCUSD',
        'BTCEUR' : 'BTCEUR',
        'ETHBTC' : 'ETHBTC'
    }

    @classmethod
    def _quote_extractor(cls, data, underlying, quote):
        return data.get(cls.QUOTE_DICT[quote])
