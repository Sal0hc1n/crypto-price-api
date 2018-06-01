from exchanges.tools.base import Exchange

class GDAX(Exchange):
    name = 'gdax'
    TICKER_URL = 'https://api.gdax.com/products/%s/ticker'
    UNDERLYING_DICT = {
        'BTCUSD' : 'BTC-USD',
        'BTCEUR' : 'BTC-EUR',
        'ETHUSD' : 'ETH-USD',
        'ETHEUR' : 'ETH-EUR',
        'ETHBTC' : 'ETH-BTC'
    }

    QUOTE_DICT = {
        'last' : 'price',
        'bid' : 'bid',
        'ask' : 'ask'
    }

    @classmethod
    def _quote_extractor(cls, data, underlying, quote):
        return data.get(cls.QUOTE_DICT[quote])
