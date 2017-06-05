from exchanges.base import Exchange
import requests

class GateCoin(Exchange):

    TICKER_URL = 'https://api.gatecoin.com/Public/LiveTickers'
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

