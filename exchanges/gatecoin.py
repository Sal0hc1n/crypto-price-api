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
        'ETHEUR' : 'ETHEUR'
    }

    @classmethod
    def _quote_extractor(cls, data, underlying, quote):
        for jsonitem in data.get('tickers'):
            if jsonitem.get('currencyPair') == cls.UNDERLYING_DICT[underlying]:
                return jsonitem.get(cls.QUOTE_DICT[quote])

    @classmethod
    def get_depth(cls, underlying, size):
        ticker = "https://api.gatecoin.com/Public/MarketDepth/%s" % underlying
        r = requests.get(ticker)
        r.raise_for_status()
        jsonitem = r.json()
        asks = [[x['volume'],x['price']] for x in jsonitem['asks']]
        bids = [[x['volume'],x['price']] for x in jsonitem['bids']]
        ask_size = 0
        ask = 0
        i = 0
        while (ask_size < size and i<len(asks)):
            prev_size = ask_size
            prev = prev_size * ask
            ask_size += asks[i][0]
            ask_size = min(size, ask_size)
            ask = ((ask_size - prev_size) *asks[i][1] + prev)/(ask_size)
            i+=1
        bid_size=0
        bid=0
        i=0
        while (bid_size < size and i<len(bids)):
            prev_size = bid_size
            prev = prev_size * bid
            bid_size += bids[i][0]
            bid_size = min(size, bid_size)
            bid = ((bid_size - prev_size) *bids[i][1] + prev)/(bid_size)
            i+=1
        return [bid, ask, bid_size, ask_size]

    # Send requests via the private API
    def _send_request(self, command, httpMethod, params={}):
        now = str(time.time())
        contentType = "" if httpMethod == "GET" else "application/json"
        url = self.API_URL + command
        message = httpMethod + url + contentType + now
        message = message.lower()
        if self.get_secret() == None:
            print("GateCoin credentials not found. Check your config.ini")
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
        #print("command: %r" % command)
        #print("url: %r" % url)
        #print("headers: %r" % headers)
        #print("params: %r" % params)
        #print("message: %r" % message)
        #print("data: %r\n" % data)
        response = R(url, data=data, headers=headers)
        #print("response: %r\n" % response.content)
        try:
            return response.json()
        except ValueError as err:
            print(str(url) + ":" + str(response) + ", " + str(err))
            return None

    def buy(self, underlying, amount, price):
        return self.place_order(underlying, str(amount), str(price), "BID")

    def sell(self, underlying, amount, price):
        return self.place_order(underlying, str(amount), str(price), "ASK")

    def place_order(self, underlying, amount, price, type):
        data = {'Code': underlying, 'Way': type, 'Amount': amount, 'Price': price}
        order = self._send_request("Trade/Orders", "POST", data)
        if order['responseStatus']['message'] == 'OK':
            return order['clOrderId']
        else:
            return "ERROR: order %s %s %s at %s Not Placed" % (type, amount, underlying, amount)

    def delete_order(self, order_id):
        return self._send_request("Trade/Orders/"+order_id, "DELETE")

    def get_balances(self):
        return self._send_request("Balance/Balances", "GET")

    # look for order done in trade_count last transactions
    def is_order_done(self, order_id, trade_count = 0):
        if trade_count == 0:
            req = "Trade/Trades"
        else:
            req = "Trade/Trades?Count=%s" % int(trade_count)
        data = self._send_request(req,"GET")
        if data == None:
            return None
        elif data['responseStatus']['message'] == 'OK':
            transaction_list = [x['bidOrderID'] if x['way'] == 'Bid' else x['askOrderID'] for x in data['transactions']]
            return order_id in transaction_list
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

