from exchanges.tools.base import Exchange
from exchanges.tools.helpers import get_response

from datetime import datetime, timedelta
from decimal import Decimal



class Gemini(Exchange):
    name = 'gemini'
    TICKER_URL = 'https://api.gemini.com/v1/pubticker/btcusd'
    UNDERLYING_DICT = {
        'BTCUSD' : 'btcusd',
        'ETHUSD' : 'ethusd',
        'ETHBTC' : 'ethbtc'
    }

    @classmethod
    def _current_price_extractor(cls, data):
        return data.get('last')

    @classmethod
    def _current_bid_extractor(cls, data):
        return data.get('bid')

    @classmethod
    def _current_ask_extractor(cls, data):
        return data.get('ask')

    @classmethod
    def get_historical_data_as_dict(cls, start='2013-09-01'):
        start_date = datetime.strptime(start, '%Y-%m-%d')
        delta = datetime.today() - start_date
        days = [start_date + timedelta(x) for x in range(delta.days + 1)]
        data = map(cls._get_historical_data, days)
        prices = {datetime.strftime(k, '%Y-%m-%d'): Decimal(str(v['price']))
                  for (k,v) in zip(days, data)}
        return prices

    @classmethod
    def get_historical_data_as_list(cls, start='2013-09-01'):
        pass
        start_date = datetime.strptime(start, '%Y-%m-%d')
        delta = datetime.today() - start_date
        days = [start_date + timedelta(x) for x in range(delta.days + 1)]
        data = map(lambda day: cls._get_historical_data(day), days)
        ret = [
            {'date': datetime.strftime(k, '%Y-%m-%d'),
             'price': Decimal(str(v['price']))}
            for (k,v) in zip(days, data)
        ]
        return ret

    @classmethod
    def _get_historical_data(cls, day):
        url = 'https://api.gemini.com/v1/trades/btcusd?since=%s&limit_trades=1'
        return get_response(url % day.strftime('%s'))[0]

    @classmethod
    def _quote_extractor(cls, data, underlying, quote):
        return data.get(cls.QUOTE_DICT[quote])
