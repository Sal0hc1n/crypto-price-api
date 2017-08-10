from exchanges.base import Exchange


class Bitfinex(Exchange):

    TICKER_URL = 'https://api.bitfinex.com/v1/pubticker/%s'
    UNDERLYING_DICT = {
        'BTCUSD' : 'btcusd',
        'ETHBTC' : 'ethbtc',
        'XRPBTC' : 'xrpbtc',
        'ETHUSD' : 'ethusd',
        'EOSETH' : 'eoseth',
        'EOSUSD' : 'eosusd',
        'EOSBTC' : 'eosbtc',
        'OMGBTC' : 'omgbtc',
        'OMGUSD' : 'omgusd',
        'OMGETH' : 'omgeth',
        'BCCBTC' : 'bccbtc',
        'BCCUSD' : 'bccusd'
    }
    QUOTE_DICT = {
        'last' : 'last_price',
        'bid' : 'bid',
        'ask' : 'ask'
    }

    @classmethod
    def _quote_extractor(cls, data, underlying, quote):
        return data.get(cls.QUOTE_DICT[quote])


