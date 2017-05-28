from decimal import Decimal

from exchanges.helpers import get_response


class Coinapult(object):

    TICKER_URL = 'https://api.coinapult.com/api/ticker?market={}_BTC'
    TICKER_LEVEL = [
        (50, 'small'),
        (250, 'medium'),
        (1000, 'large'),
        (2500, 'vip'),
        (5000, 'vip+')
    ]
    SUPPORTED_UNDERLYINGS=['BTCUSD']

    @classmethod
    def get_last_price(cls, underlying):
        url = cls.TICKER_URL.format('USD')
        data = get_response(url)
        price = str(data['index'])
        return Decimal(price)

    @classmethod
    def get_current_bid(cls, underlying, btc_amount=0.1):
        url = cls.TICKER_URL.format('USD')
        data = get_response(url)
        level = cls._pick_level(btc_amount) if btc_amount > 0 else 'small'
        price = str(data[level]['bid'])
        return Decimal(price)

    @classmethod
    def get_current_ask(cls, underlying, btc_amount=0.1):
        url = cls.TICKER_URL.format('USD')
        data = get_response(url)
        level = cls._pick_level(btc_amount) if btc_amount > 0 else 'small'
        price = str(data[level]['ask'])
        return Decimal(price)

    @classmethod
    def get_supported_underlyings(cls):
        return cls.SUPPORTED_UNDERLYINGS

    @classmethod
    def _pick_level(cls, btc_amount):
        """
        Choose between small, medium, large, ... depending on the
        amount specified.
        """
        for size, level in cls.TICKER_LEVEL:
            if btc_amount < size:
                return level
        return cls.TICKER_LEVEL[-1][1]
