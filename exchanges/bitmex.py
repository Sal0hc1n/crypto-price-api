from decimal import Decimal

import time, base64, hmac, json, hashlib, requests, uuid
from urlparse import urlparse

from exchanges.base import Exchange
from exchanges.ws import Exchange_WebSocket
import logging

class BitMEX(Exchange):

    TICKER_URL = 'https://www.bitmex.com/api/v1/'
    WS_TICKER_URL = 'https://www.bitmex.com/api/v1/'
    stream = {}

    QUOTE_DICT = {
        'bid' : 'bidPrice',
        'ask' : 'askPrice'
    }

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

    def get_quote(self, symbol, quote):
        if symbol in self.stream.keys():
            if self.stream[symbol].connected:
                try:
                    return self.stream[symbol].data['quote'][-1:][0][self.QUOTE_DICT[quote]]
                except KeyError as err:
                    return "Undefined key: %s" % err
            else:
                return "Not connected"
        else:
            return None

    def get_stream(self, symbol):
        if symbol in self.stream.keys():
            if self.stream[symbol].connected:
                return self.stream[symbol]
            else:
                return "Not connected"
        else:
            return None

    def delete_order(self, order_id):
        self.logger.info("Cancelling order %s" % order_id)
        params = {'clOrdID': order_id}
        return self._send_request('order','DELETE',params)

    def place_order(self, symbol, quantity, price):
        if price < 0:
            self.logger.error("Price must be postive")
            return None
        clOrdID = self.name + base64.b64encode(uuid.uuid4().bytes).decode('utf-8').rstrip('=\n')
        params = {'symbol': symbol, 'orderQty': quantity, 'price': price, 'clOrdID' : clOrdID}
        return self._send_request('order','POST',params)

    def buy(self, symbol, quantity, price):
        return self.place_order(symbol, quantity, price)

    def sell(self, symbol, quantity, price):
        return self.place_order(symbol, -quantity, price)

    def _send_request(self, command, httpMethod, params={}):
        contentType = "" if httpMethod == "GET" else "application/json"
        url = self.TICKER_URL + command
        now = time.time()
        nonce = int(round(now * 1000))
        data = json.dumps(params)
        parsedURL = urlparse(url)
        path = parsedURL.path
        if parsedURL.query:
            path = path + '?' + parsedURL.query
        message = httpMethod + path + str(nonce) + data
        if self.get_secret() == None:
            self.logger.error("Credentials not found. Check your config.ini")
            self.error = "AuthFailed"
            return None
        signature = hmac.new(self.get_secret().encode(), message.encode(), digestmod=hashlib.sha256).hexdigest()
        headers = {
            'api-nonce' : str(nonce),
            'api-key' : self.get_key(),
            'api-signature' : signature,
            'Content-Type' : contentType
        }
        if httpMethod == 'DELETE':
            R = requests.delete
        elif httpMethod == 'GET':
            R = requests.get
        elif httpMethod == 'POST':
            R = requests.post
        try:
            response = R(url, data=data, headers=headers)
        except requests.exceptions.ConnectionError as err:
            self.logger.debug("command: %r" % command)
            self.logger.debug("url: %r" % url)
            self.logger.debug("headers: %r" % headers)
            self.logger.debug("params: %r" % params)
            self.logger.debug("message: %r" % message)
            self.logger.debug("data: %r" % data)
            self.logger.error(err)
            return None
        try:
            return response.json()
        except ValueError as err:
            self.logger.error(str(url) + ":" + str(response) + ", " + str(err))
            return None

