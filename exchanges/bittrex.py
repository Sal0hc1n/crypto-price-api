from exchanges.base import Exchange


class Bittrex(Exchange):

    TICKER_URL = 'https://bittrex.com/api/v1.1/public/getticker?market=USDT-BTC'

    @classmethod
    def _current_price_extractor(cls, data):
        return data.get('result').get('Last')

    @classmethod
    def _current_bid_extractor(cls, data):
        return data.get('result').get('Bid')

    @classmethod
    def _current_ask_extractor(cls, data):
        return data.get('result').get('Ask')
