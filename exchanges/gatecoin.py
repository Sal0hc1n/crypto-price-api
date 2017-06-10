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
        return response.json()

    def buy(self, underlying, amount, price):
        return self.place_order(underlying, str(amount), str(price), "BID")

    def sell(self, underlying, amount, price):
        return self.place_order(underlying, str(amount), str(price), "ASK")

    def place_order(self, underlying, amount, price, type):
        data = {'Code': underlying, 'Way': type, 'Amount': amount, 'Price': price}
        return self._send_request("Trade/Orders", "POST", data)

    def delete_order(self, order_id):
        return self._send_request("Trade/Orders/"+order_id, "DELETE")

    def get_balances(self):
        return self._send_request("Balance/Balances", "GET")

    def get_balance(self, currency):
        return self._send_request("Balance/Balances/%s" % currency, "GET")

