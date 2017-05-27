from exchanges.base import Exchange


class GateCoin(Exchange):

    TICKER_URL = 'https://api.gatecoin.com/Public/LiveTickers'

    @classmethod
    def _current_price_extractor(cls, data):
        for jsonitem in data.get('tickers'):
            if jsonitem.get('currencyPair') == 'BTCUSD':
                return jsonitem.get('last')

    @classmethod
    def _current_bid_extractor(cls, data):
        for jsonitem in data.get('tickers'):
            if jsonitem.get('currencyPair') == 'BTCUSD':
                return jsonitem.get('bid')

    @classmethod
    def _current_ask_extractor(cls, data):
        for jsonitem in data.get('tickers'):
            if jsonitem.get('currencyPair') == 'BTCUSD':
                return jsonitem.get('ask')
