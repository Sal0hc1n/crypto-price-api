import datetime
import ConfigParser
import os
from decimal import Decimal
import logging

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

    def __init__(self, exchangeName, loggerObject = None, *args, **kwargs):
        if type(loggerObject) is not logging.getLoggerClass():
            self.logger = logging.getLogger(exchangeName)
            # default log to stdout. override this if needed
            self.logger.setLevel(logging.DEBUG)
            lh = logging.StreamHandler()
            lh.setFormatter(logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"))
            self.logger.addHandler(lh)
        else:
            self.logger = loggerObject
        self.data = None
        self.error = ''
        self.name = exchangeName
        self.ticker_url = self.TICKER_URL
        self.underlying_dict = self.UNDERLYING_DICT
        self.quote_dict = self.QUOTE_DICT
        c = ConfigParser.ConfigParser()
        cPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini')
        self.logger.debug("Loading %s" % cPath)
        c.read(cPath)
        try:
            self.key = c.get(self.name,'key')
            self.secret = c.get(self.name,'secret')
        except ConfigParser.NoSectionError as err:
            self.error = str(err)
            self.key = None
            self.secret = None

    def get_key(self):
        return self.key

    def has_error(self):
        return self.error != ''

    def get_error(self):
        if self.error == '':
            return None
        else:
            return self.error

    def get_secret(self):
        return self.secret

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
        if self.data == None:
            return 0
        else:
            quote = self._quote_extractor(self.data, underlying, quote)
        if quote is None:
            return 0
        else:
            return Decimal(quote)

    def get_supported_underlyings(self):
        return sorted(self.underlying_dict.keys())

    def get_supported_quotes(self):
        return sorted(self.quote_dict.keys())

class FuturesExchange(ExchangeBase):

    def get_current_data(cls):
        raise NotImplementedError
