from exchanges.tools.base import Exchange

class Bitstamp(Exchange):
    name = 'bitstamp'
    TICKER_URL = 'https://bitstamp.net/api/v2/ticker/%s/'
    UNDERLYING_DICT = {
        'BTCUSD' : 'btcusd',
        'BTCEUR' : 'btceur',
        'XRPBTC' : 'xrpbtc',
        'ETHUSD' : 'ethusd',
        'ETHEUR' : 'etheur',
        'ETHBTC' : 'ethbtc',
        'XRPEUR' : 'xrpeur',
        'XRPUSD' : 'xrpusd'
    }

    @classmethod
    def _quote_extractor(cls, data, underlying, quote):
        return data.get(cls.QUOTE_DICT[quote])
