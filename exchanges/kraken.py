from exchanges.tools.base import Exchange

class Kraken(Exchange):
    name = 'kraken'
    TICKER_URL = 'https://api.kraken.com/0/public/Ticker?pair=%s'
    UNDERLYING_DICT = {
        'BTCUSD' : 'XXBTZUSD',
        'BTCEUR' : 'XXBTZEUR',
        'ETHBTC' : 'XETHXXBT',
        'BTCJPY' : 'XXBTZJPY',
        'ETHJPY' : 'XETHZJPY',
        'ETHUSD' : 'XETHZUSD',
        'ETHEUR' : 'XETHZEUR',
        'EOSBTC' : 'EOSXBT',
        'EOSETH' : 'EOSETH',
        'USDTUSD' : 'USDTZUSD',
        'DASHUSD' : 'DASHUSD',
        'DASHBTC' : 'DASHXBT',
        'ICNBTC' : 'XICNXXBT',
        'ICNETH' : 'XICNXETH',
        'XMRUSD' : 'XXMRZUSD',
        'XMRBTC' : 'XXMRXXBT',
        'BCHBTC' : 'BCHXBT',
        'BCHUSD' : 'BCHUSD',
        'BCHEUR' : 'BCHEUR'
    }

    QUOTE_DICT = {
        'ask' : 'a',
        'bid' : 'b',
        'last' : 'c'
    }

    def _quote_extractor(cls, data, underlying, quote):
        if data.get('result') is None:
            cls.logger.error(data)
            return None
        else:
            return data.get('result').get(cls.UNDERLYING_DICT[underlying]).get(cls.QUOTE_DICT[quote])[0]
