from exchanges.base import Exchange


class CexIO(Exchange):

    TICKER_URL = 'https://cex.io/api/ticker/BTC/USD'
    SUPPORTED_UNDERLYINGS = ['BTCUSD']

    @classmethod
    def _last_price_extractor(cls, data, underlying):
        return data.get('last')

    @classmethod
    def _current_bid_extractor(cls, data, underlying):
        return data.get('bid')

    @classmethod
    def _current_ask_extractor(cls, data, underlying):
        return data.get('ask')
