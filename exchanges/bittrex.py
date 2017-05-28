from exchanges.base import Exchange

class Bittrex(Exchange):

    TICKER_URL = 'https://bittrex.com/api/v1.1/public/getticker?market=%s'
    SUPPORTED_UNDERLYINGS = ['BTCUSD','ETHBTC']
    UNDERLYING_DICT = {
        'BTCUSD' : 'USDT-BTC',
        'ETHBTC' : 'BTC-ETH'
    }
    QUOTE_DICT = {
        'bid' : 'Bid',
        'ask' : 'Ask',
        'last' : 'Last'
    }

    @classmethod
    def _quote_extractor(cls, data, underlying, quote):
        return data.get('result').get(cls.QUOTE_DICT[quote])
