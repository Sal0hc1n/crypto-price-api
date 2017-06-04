from exchanges.base import Exchange

class Bitstamp(Exchange):

    TICKER_URL = 'https://bitstamp.net/api/v2/ticker/%s/'
    UNDERLYING_DICT = {
        'BTCUSD' : 'btcusd',
        'BTCEUR' : 'btceur',
        'XRPBTC' : 'xrpbtc',
        'XRPEUR' : 'xrpeur',
        'XRPUSD' : 'xrpusd'
    }

    @classmethod
    def _quote_extractor(cls, data, underlying, quote):
        return data.get(cls.QUOTE_DICT[quote])
