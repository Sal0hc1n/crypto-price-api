from exchanges.tools.base import Exchange, date_stamp, time_stamp
from exchanges.tools.helpers import get_response, get_datetime

from decimal import Decimal

import requests
import datetime

class OKCoin(Exchange):
    name = 'okcoin'
    TICKER_URL = 'https://www.okcoin.com/api/v1/ticker.do?symbol=%s'
    UNDERLYING_DICT = {
        'BTCUSD' : 'btc_usd',
        'ETHUSD' : 'eth_usd'
    }
    QUOTE_DICT = {
        'bid' : 'buy',
        'ask' : 'sell',
        'last' : 'last'
    }

    @classmethod
    def _quote_extractor(cls, data, underlying, quote):
        return data.get('ticker', {}).get(cls.QUOTE_DICT[quote])

class OKCoinFutures(Exchange):

    @classmethod
    def get_current_data(cls):
        symbols = []
        dates = []
        bids = []
        asks = []
        last = []
        contract = []
        for i in ['this_week', 'next_week', 'month', 'quarter']:
            response = requests.get(
                'https://www.okcoin.com/api/future_ticker.do',
                params={
                    'symbol': 'btc_usd',
                    'contractType': i
                }
            )
            data = response.json()['ticker'][0]
            d = datetime.date(
                int(str(data['contractId'])[0:4]),
                int(str(data['contractId'])[4:6]),
                int(str(data['contractId'])[6:8])
            )
            dates.append(date_stamp(d))
            bids.append(data['buy'])
            asks.append(data['sell'])
            last.append(data['last'])
            contract.append('XBT')

        return {
            'contract' : contract,
            'dates': dates,
            'bids' : [Decimal(str(x)) for x in bids],
            'asks' : [Decimal(str(x)) for x in asks],
            'last' : [Decimal(str(x)) for x in last]
        }
