from exchanges.base import Exchange

class Liqui(Exchange):

    TICKER_URL = 'https://api.liqui.io/api/3/ticker/%s'
    UNDERLYING_DICT = {
        'ETHBTC' : 'eth_btc',
        'SNTETH' : 'snt_eth',
        'SNTBTC' : 'snt_btc',
        'ETHUSDT' : 'eth_usdt',
        'BTCUSDT' : 'btc_usdt',
        'EOSBTC' : 'eos_btc',
        'EOSETH' : 'eos_eth',
        'PAYETH' : 'pay_eth',
        'PAYBTC' : 'pay_btc'
    }

    QUOTE_DICT = {
        'bid' : 'buy',
        'ask' : 'sell',
        'last' : 'last'
    }

    @classmethod
    def _quote_extractor(cls, data, underlying, quote):
        return data[cls.UNDERLYING_DICT[underlying]][cls.QUOTE_DICT[quote]]
