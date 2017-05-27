from exchanges.base import Exchange


class BitBay(Exchange):

    TICKER_URL = 'https://bitbay.net/API/Public/BTCUSD/ticker.json'

    @classmethod
    def _current_price_extractor(cls, data):
        return data.get('last')

    @classmethod
    def _current_bid_extractor(cls, data):
        return data.get('bid')

    @classmethod
    def _current_ask_extractor(cls, data):
        return data.get('ask')
