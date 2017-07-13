from exchanges.base import Exchange
import time, base64, hmac, json, hashlib, requests

class GateCoin(Exchange):

    TICKER_URL = 'https://api.gatecoin.com/Public/LiveTickers'
    API_URL = 'https://api.gatecoin.com/'
    UNDERLYING_DICT = {
        'BTCUSD' : 'BTCUSD',
        'BTCEUR' : 'BTCEUR',
        'BTCHKD' : 'BTCHKD',
        'ETHBTC' : 'ETHBTC',
        'ETHEUR' : 'ETHEUR',
        'ETHUSD' : 'ETHUSD',
        'ETHHKD' : 'ETHHKD',
        'SNTUSD' : 'SNTUSD',
        'SNTBTC' : 'SNTBTC',
        'PAYBTC' : 'PAYBTC',
        'PAYETH' : 'PAYETH'
    }

    @classmethod
    def _quote_extractor(cls, data, underlying, quote):
        for jsonitem in data.get('tickers'):
            if jsonitem.get('currencyPair') == cls.UNDERLYING_DICT[underlying]:
                return jsonitem.get(cls.QUOTE_DICT[quote])

    def get_depth(cls, underlying, bid_size = 0, ask_size = 0):
        ticker = "https://api.gatecoin.com/Public/MarketDepth/%s" % underlying
        try:
            r = requests.get(ticker)
            r.raise_for_status()
            jsonitem = r.json()
        except requests.exceptions.ReadTimeout as err:
            cls.logger.error(err)
            return [0,0,0,0]
        except requests.exceptions.HTTPError as err:
            cls.logger.error(err)
            return [0,0,0,0]
        except requests.exceptions.SSLError as err:
            cls.logger.error(err)
            cls.logger.error("Consider upgrading OpenSSL")
            return [0,0,0,0]
        except requests.exceptions.ConnectionError as err:
            cls.logger.error(err)
            return [0,0,0,0]
        asks = [[x['volume'],x['price']] for x in jsonitem['asks']]
        bids = [[x['volume'],x['price']] for x in jsonitem['bids']]
        work_ask_size = 0
        ask = 0
        i = 0
        if len(bids) == 0 or len(asks) == 0:
            cls.logger.error("Unable to retrieve quotes for %s" % underlying)
            return [0,0,0,0]
        while (work_ask_size <= ask_size and i<len(asks)):
            prev_size = work_ask_size
            prev = prev_size * ask
            work_ask_size += asks[i][0]
            if ask_size != 0:
                work_ask_size = min(ask_size, work_ask_size)
            ask = ((work_ask_size - prev_size) *asks[i][1] + prev)/(work_ask_size)
            i+=1
        work_bid_size=0
        bid=0
        i=0
        while (work_bid_size <= bid_size and i<len(bids)):
            prev_size = work_bid_size
            prev = prev_size * bid
            work_bid_size += bids[i][0]
            if bid_size != 0:
                work_bid_size = min(bid_size, work_bid_size)
            bid = ((work_bid_size - prev_size) *bids[i][1] + prev)/(work_bid_size)
            i+=1
        return [bid, ask, work_bid_size, work_ask_size]

    # Send requests via the private API
    def _send_request(self, command, httpMethod, params={}):
        now = str(time.time())
        contentType = "" if httpMethod == "GET" else "application/json"
        url = self.API_URL + command
        message = httpMethod + url + contentType + now
        message = message.lower()
        if self.get_secret() == None:
            self.logger.error("Credentials not found. Check your config.ini")
            self.error = "AuthFailed"
            return None
        signature = hmac.new(self.get_secret().encode(), msg=message.encode(), digestmod=hashlib.sha256).digest()
        hashInBase64 = base64.b64encode(signature, altchars=None)
        headers = {
            'API_PUBLIC_KEY': self.get_key(),
            'API_REQUEST_SIGNATURE': hashInBase64,
            'API_REQUEST_DATE': now,
            'Content-Type':'application/json'
        }
        data = None
        if httpMethod == "DELETE":
            R = requests.delete
        elif httpMethod == "GET":
            R = requests.get
        elif httpMethod == "POST":
            R = requests.post
        data = json.dumps(params)
        #self.logger.debug("command: %r" % command)
        #self.logger.debug("url: %r" % url)
        #self.logger.debug("headers: %r" % headers)
        #self.logger.debug("params: %r" % params)
        #self.logger.debug("message: %r" % message)
        #self.logger.debug("data: %r\n" % data)
        try:
            response = R(url, data=data, headers=headers)
        except requests.exceptions.ConnectionError as err:
            self.logger.debug("command: %r" % command)
            self.logger.debug("url: %r" % url)
            self.logger.debug("headers: %r" % headers)
            self.logger.debug("params: %r" % params)
            self.logger.debug("message: %r" % message)
            self.logger.debug("data: %r\n" % data)
            self.logger.error(err)
            return None
        try:
            return response.json()
        except ValueError as err:
            self.logger.error(str(url) + ":" + str(response) + ", " + str(err))
            return None

    def buy(self, underlying, amount, price):
        return self.place_order(underlying, str(amount), str(price), "BID")

    def sell(self, underlying, amount, price):
        return self.place_order(underlying, str(amount), str(price), "ASK")

    def place_order(self, underlying, amount, price, type):
        data = {'Code': underlying, 'Way': type, 'Amount': amount, 'Price': price}
        order = self._send_request("Trade/Orders", "POST", data)
        if order == None:
            self.logger.error("ERROR: order %s %s %s at %s not placed: %s" % (type, amount, underlying, price, str(order)))
            return -1
        if order['responseStatus']['message'] == 'OK':
            return order['clOrderId']
        else:
            self.logger.error("ERROR: order %s %s %s at %s not placed: %s" % (type, amount, underlying, price, str(order)))
            return -1

    def delete_order(self, order_id):
        return self._send_request("Trade/Orders/%s" % order_id, "DELETE")

    def get_balances(self):
        return self._send_request("Balance/Balances", "GET")

    def get_live_orders(self):
        data = self._send_request("Trade/Orders","GET")
        if data == None:
            return None
        elif data['responseStatus']['message'] == 'OK':
            return data['orders']
        else:
            self.logger.error(str(data))
            return None

    # look for order done in trade_count last transactions
    def is_order_done(self, order_id):
        data = self._send_request("Trade/Orders/%s" % order_id,"GET")
        if data == None:
            return None
        elif data['responseStatus']['message'] == 'OK':
            return int(data['order']['status']) == 6
        else:
            return None

    def get_order_status(self, order_id):
        data = self._send_request("Trade/Orders/%s" % order_id,"GET")
        if data == None:
            return None
        elif data['responseStatus']['message'] == 'OK':
            return [int(data['order']['status']), float(data['order']['initialQuantity']) - float(data['order']['remainingQuantity'])]
        else:
            return None

    def get_trades(self, trade_count = 0):
        req = "Trade/Trades"
        if trade_count != 0:
            req += "?Count=%s" % int(trade_count)
        else:
            req += "?Count=1000"
        data = self._send_request(req, "GET")
        if data == None:
            return None
        elif data['responseStatus']['message'] == 'OK':
            trade_list = data['transactions']
            count = len(data['transactions'])
            self.logger.debug("%s transactions downloaded" % count)
            if count == 1000 and (trade_count > 1000 or trade_count == 0):
                finished = False
                while not finished:
                    req = "Trade/UserTrades?after=%s" % count
                    data = self._send_request(req,"GET")
                    if data == None:
                        self.logger.error("Error when getting additional trades")
                        return None
                    elif data['responseStatus']['message'] == 'OK':
                        if data['transactions'] == []:
                            finished = True
                        else:
                            self.logger.debug('Downloaded %s transactions, getting more...' % len(trade_list))
                            new_trade_count = len(data['transactions'])
                            if count + new_trade_count > trade_count and trade_count != 0:
                                cut = abs(trade_count - count - new_trade_count)
                                trade_list.extend(data['transactions'][:cut])
                                finished = True
                            else:
                                trade_list.extend(data['transactions'])
                                count += 50
                    else:
                        self.logger.error("Error when getting additional trades")
                        return None
            return trade_list
        else:
            return None

    def get_balance(self, currency):
        data = self._send_request("Balance/Balances/%s" % currency, "GET")
        balance = {
            'available' : 0,
            'restricted' : 0,
            'total' : 0
        }
        if data == None:
            return None
        elif data['responseStatus']['message'] == 'OK':
            balance['available'] = data['balance']['availableBalance']
            balance['total'] = data['balance']['balance']
            balance['restricted'] = balance['total'] - balance['available']
            return balance
        else:
            return data['responseStatus']['message']

