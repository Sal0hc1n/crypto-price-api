from exchanges.tools.base import Exchange

class Bittrex(Exchange):

    TICKER_URL = 'https://bittrex.com/api/v1.1/public/getticker?market=%s'
    UNDERLYING_DICT = {
        'BTCUSDT' : 'USDT-BTC',
        'ETHBTC' : 'BTC-ETH',
        'SNTBTC' : 'BTC-SNT',
        'SNTETH' : 'ETH-SNT',
        'PAYETH' : 'ETH-PAY',
        'PAYBTC' : 'BTC-PAY',
        'CVCBTC' : 'BTC-CVC',
        'XMRBTC' : 'BTC-XMR',
        'OMGBTC' : 'BTC-OMG',
        'BCHBTC' : 'BTC-BCC',
        'SCBTC' : 'BTC-SC',
        'XRPBTC' : 'BTC-XRP',
        'ADABTC' : 'BTC-ADA',
        'MUSICBTC' : 'BTC-MUSIC'
    }
    QUOTE_DICT = {
        'bid' : 'Bid',
        'ask' : 'Ask',
        'last' : 'Last'
    }

    @classmethod
    def _quote_extractor(cls, data, underlying, quote):
        return data.get('result').get(cls.QUOTE_DICT[quote])
