from exchanges.base import Exchange


class GateCoin(Exchange):

    TICKER_URL = 'https://api.gatecoin.com/Public/LiveTickers'

    SUPPORTED_UNDERLYINGS = ['BTCUSD', 'BTCEUR', 'ETHBTC']

    @classmethod
    def _last_price_extractor(cls, data, underlying):
        for jsonitem in data.get('tickers'):
            if jsonitem.get('currencyPair') == underlying:
                return jsonitem.get('last')

    @classmethod
    def _current_bid_extractor(cls, data, underlying):
        for jsonitem in data.get('tickers'):
            if jsonitem.get('currencyPair') == underlying:
                return jsonitem.get('bid')

    @classmethod
    def _current_ask_extractor(cls, data, underlying):
        for jsonitem in data.get('tickers'):
            if jsonitem.get('currencyPair') == underlying:
                return jsonitem.get('ask')
