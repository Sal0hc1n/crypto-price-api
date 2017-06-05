from exchanges.base import Exchange

class GateCoin(Exchange):

    TICKER_URL = 'https://api.gatecoin.com/Public/LiveTickers'
    UNDERLYING_DICT = {
        'BTCUSD' : 'BTCUSD',
        'BTCEUR' : 'BTCEUR',
        'BTCHKD' : 'BTCHKD',
        'ETHBTC' : 'ETHBTC',
        'ETHEUR' : 'ETHEUR'
    }

    @classmethod
    def _quote_extractor(cls, data, underlying, quote):
        for jsonitem in data.get('tickers'):
            if jsonitem.get('currencyPair') == cls.UNDERLYING_DICT[underlying]:
                return jsonitem.get(cls.QUOTE_DICT[quote])
