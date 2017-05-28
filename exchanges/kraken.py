from decimal import Decimal

from exchanges.base import Exchange
from exchanges.helpers import get_response


class Kraken(Exchange):

    TICKER_URL = 'https://api.kraken.com/0/public/Trades?pair=%s'
    DEPTH_URL = 'https://api.kraken.com/0/public/Depth?pair=%s'
    SUPPORTED_UNDERLYINGS = ['BTCUSD']

    @classmethod
    def get_last_price(cls, underlying):
        data = get_response(cls.TICKER_URL %  'XXBTZUSD')
        price = data['result']['XXBTZUSD'][-1][0]
        return Decimal(str(price))

    @classmethod
    def get_current_bid(cls, underlying):
        data = get_response(cls.DEPTH_URL % 'XXBTZUSD')
        price = data['result']['XXBTZUSD']['bids'][0][0]
        return Decimal(str(price))

    @classmethod
    def get_current_ask(cls, underlying):
        data = get_response(cls.DEPTH_URL % 'XXBTZUSD')
        price = data['result']['XXBTZUSD']['asks'][0][0]
        return Decimal(str(price))
