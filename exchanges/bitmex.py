from decimal import Decimal

import dateutil.parser

from exchanges.base import FuturesExchange, date_stamp, time_stamp
from exchanges.helpers import get_response, get_datetime
from exchanges.ws import Exchange_WebSocket
import logging

class BitMEX(FuturesExchange):

    TICKER_URL = 'https://www.bitmex.com:443/api/v1/instrument/active'
    WS_TICKER_URL = 'https://www.bitmex.com/api/v1/'
    stream = {}

    def init_symbol(self, symbol):
        self.logger.setLevel(logging.INFO)
        if symbol in self.stream.keys():
            if (not self.stream[symbol].connected) or self.stream[symbol].exited:
                ws = Exchange_WebSocket(self.name, self.key, self.secret, self.logger)
                ws.connect(self.WS_TICKER_URL)
                self.stream[symbol] = ws
        else:
            self.stream[symbol] = Exchange_WebSocket(self.name, self.key, self.secret, self.logger)
            self.stream[symbol].connect(self.WS_TICKER_URL)
        return self.stream[symbol].connected

    def get_quote(self, symbol):
        if symbol in self.stream.keys():
            if self.stream[symbol].connected:
                return self.stream[symbol].data['quote'][-1:]
        else:
            return None

