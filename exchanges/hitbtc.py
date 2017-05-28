from exchanges.base import Exchange


class HitBTC(Exchange):

    TICKER_URL = 'https://api.hitbtc.com/api/1/public/BTCUSD/ticker'
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
