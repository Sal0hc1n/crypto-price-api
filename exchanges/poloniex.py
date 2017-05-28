from exchanges.base import Exchange


class Poloniex(Exchange):

    TICKER_URL = 'https://poloniex.com/public?command=returnTicker'
    SUPPORTED_UNDERLYINGS = ['BTCUSD']

    @classmethod
    def _last_price_extractor(cls, data, underlying):
        return data.get('USDT_BTC').get('last')

    @classmethod
    def _current_bid_extractor(cls, data, underlying):
        return data.get('USDT_BTC').get('highestBid')

    @classmethod
    def _current_ask_extractor(cls, data, underlying):
        return data.get('USDT_BTC').get('lowestAsk')
