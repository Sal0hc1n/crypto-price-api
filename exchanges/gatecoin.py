from exchanges.base import Exchange

class GateCoin(Exchange):

    TICKER_URL = 'https://api.gatecoin.com/Public/LiveTickers'
    SUPPORTED_UNDERLYINGS = ['BTCUSD', 'BTCEUR', 'ETHBTC']

    @classmethod
    def _quote_extractor(cls, data, underlying, quote):
        for jsonitem in data.get('tickers'):
            if jsonitem.get('currencyPair') == underlying:
                return jsonitem.get(cls.QUOTE_DICT[quote])
