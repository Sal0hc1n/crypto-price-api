from exchanges.base import Exchange

class GateCoin(Exchange):

    TICKER_URL = 'https://api.gatecoin.com/Public/LiveTickers'
    UNDERLYING_DICT = {
        'BTCUSD' : 'BTCUSD',
        'BTCEUR' : 'BTCEUR',
        'ETHBTC' : 'ETHBTC'
    }

    @classmethod
    def _quote_extractor(cls, data, underlying, quote):
        for jsonitem in data.get('tickers'):
            if jsonitem.get('currencyPair') == cls.underlying_dict[underlying]:
                return jsonitem.get(cls.quote_dict[quote])
