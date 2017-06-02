import datetime
from decimal import Decimal

from exchanges.helpers import get_response, get_datetime


def weekly_expiry():
    d = datetime.date.today()
    while d.weekday() != 5:
        d += datetime.timedelta(1)
    return d


def  quarter_expiry():
    ref = datetime.date.today()
    if ref.month < 4:
        d = datetime.date(ref.year, 3, 31)
    elif ref.month < 7:
        d = datetime.date(ref.year, 6, 30)
    elif ref.month < 10:
        d = datetime.date(ref.year, 9, 30)
    else:
        d= datetime.date(ref.year, 12, 31)
    while d.weekday() != 5:
        d -= datetime.timedelta(1)
    return d


def date_stamp(d):
    return d.strftime('%Y-%m-%d')


def time_stamp(d):
    return d.strftime('%H:%M:%S')


class ExchangeBase(object):

    TICKER_URL = None
    SUPPORTED_UNDERLYINGS = []
    UNDERLYING_DICT = {}
    QUOTE_DICT = {
        'bid' : 'bid',
        'ask' : 'ask',
        'last' : 'last'
    }

    def __init__(self, *args, **kwargs):
        self.data = None
        self.ticker_url = self.TICKER_URL
        self.underlying_dict = self.UNDERLYING_DICT
        self.quote_dict = self.QUOTE_DICT

    def get_data(self, underlying):
        self.refresh(underlying)

    def refresh(self, underlying, callback=None, client_data=None):
        if '%s' in self.ticker_url:
            requesturl = self.ticker_url % self.underlying_dict[underlying]
        else:
            requesturl = self.ticker_url
        self.data = get_response(requesturl)
        if callback is not None:
            callback(self, client_data)

class Exchange(ExchangeBase):

    def _quote_extractor(self, data, underlying, quote):
        raise NotImplementedError

    def get_quote(self, underlying, quote):
        self.get_data(underlying)
        quote = self._quote_extractor(self.data, underlying, quote)
        return Decimal(quote)

    def get_supported_underlyings(self):
        return sorted(self.underlying_dict.keys())

    def get_supported_quotes(self):
        return sorted(self.quote_dict.keys())

class FuturesExchange(ExchangeBase):

    def get_current_data(cls):
        raise NotImplementedError
