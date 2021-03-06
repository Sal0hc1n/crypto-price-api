#!/bin/python3
# workaround from https://github.com/requests/requests/issues/3752
import gevent.monkey
gevent.monkey.patch_ssl()
import requests
import multiprocessing
import time
import grequests

assets = ['USD', 'USDT', 'EUR', 'BTC', 'XRP', 'ETH', 'HKD', 'LTC', 'RUR',
          'CNY', 'DASH', 'ZEC', 'ETC', 'BCH']

#btce
def btc_e(assets):
    r = requests.get('https://btc-e.com/api/3/info').json()
    urls=[]
    pairs = []
    for k, v in r['pairs'].items():
        k1, k2 = k.upper().split("_")
        if k1 in assets and k2 in assets:
            pairs.append(k)
            urls.append('https://btc-e.com/api/3/ticker/' + k)
    def item(r):
        k,v = r.popitem()
        k1, k2 = k.upper().split("_")
        return {'from': k1,
                'to': k2,
                'bid': v['buy'],
                'ask': v['sell'],
                'last': v['last']}
    return [item(x.json()) for x in \
            grequests.imap([grequests.get(u) for u in urls])]

def gatecoin(assets):
    retval = []
    r = requests.get('https://api.gatecoin.com/Public/LiveTickers').json()
    for k in r['tickers']:
        s = k['currencyPair']
        k1 = s[0:3].upper()
        k2 = s[3:].upper()
        if k1 in assets and k2 in assets:
            retval.append({'from': k1,
                           'to': k2,
                           'bid': k['bid'],
                           'ask': k['ask'],
                           'last' : k['last']})
    return retval

def poloniex(assets):
    """Poloniex assets"""
    d = requests.get('https://poloniex.com/public?command=returnTicker').json()
    def in_assets(k):
        k1, k2 = k.split("_")
        return k1 in assets and k2 in assets
    def items(k, v):
        k1, k2 = k.split("_")
        return {'from': k2,
                'to': k1,
                'bid': v['highestBid'],
                'ask': v['lowestAsk'],
                'last': v['last']
                }
    return [ items(k,v) for k, v in d.items() if in_assets(k)]


def bitfinex(assets):
    """Bitfinex assets"""
    retval = []
    urls = []
    pairs = []
    bitfinex_url = 'https://api.bitfinex.com/v1'
    symbols = requests.get(bitfinex_url + '/symbols').json()
    for s in symbols:
        k1 = s[0:3].upper()
        k2 = s[3:].upper()
        if k1 == "DSH":
            k1 = "DASH"
        if k2 == "DSH":
            k2 = "DASH"
        if k1 in assets and k2 in assets:
            pairs.append(s)
            urls.append(bitfinex_url + '/pubticker/' + s)
    rs = [grequests.get(u) for u in urls]
    for i in zip(pairs, grequests.map(rs)):
        r = i[1].json()
        k = i[0]
        k1 = k[0:3].upper()
        k2 = k[3:].upper()
        retval.append({'from': k1,
                       'to': k2,
                       'bid': r['bid'],
                       'ask': r['ask'],
                       'last' : r['last_price']})
    return retval

def bitstamp(assets):
    """Bitstamp assets"""
    urls = []
    symbols = ['btcusd', 'btceur',
              'eurusd', 'xrpusd', 'xrpeur',
              'xrpbtc', 'ltcusd', 'ltceur', 'ltcbtc']
    bitstamp_url = 'https://www.bitstamp.net/api/v2/ticker/'
    for s in symbols:
        k1 = s[0:3].upper()
        k2 = s[3:].upper()
        if k1 in assets and k2 in assets:
            urls.append(bitstamp_url + s +"/")
    rs = [grequests.get(u) for u in urls]
    def item(i):
        d = i[1].json()
        k = i[0]
        k1 = k[0:3].upper()
        k2 = k[3:].upper()
        return {'from': k1,
                'to': k2,
                'bid': d['bid'],
                'ask': d['ask'],
                'last': d['last']}
    return [ item(x) for x in zip(symbols, grequests.map(rs)) ]

def bitcashout(assets):
    return [{'from':'BTC',
             'to': i['currency'].upper(),
             'bid': i['buy'],
             'ask': i['sell'],
             'last' : i['last_trade']['price']
             } for i in \
            requests.get('https://www.bitcashout.com/ticker.json').json()]

def anx(assets):
    retval = []
    urls = []
    pairs = []
    resp = requests.get('https://anxpro.com/api/3/currencyStatic').json()
    for k, v in resp['currencyStatic']['currencyPairs'].items():
        k1 = v['tradedCcy']
        k2 = v['settlementCcy']
        if k1 in assets and k2 in assets:
            pairs.append([k1, k2])
            urls.append('https://anxpro.com/api/2/%s/money/ticker' % k)
    def item(r):
        return {'from': r['vol']['currency'],
                'to': r['last']['currency'],
                'bid': float(r['buy']['value']),
                'ask': float(r['sell']['value']),
                'last': float(r['last']['value'])}
    return [item(i.json()['data']) \
            for i in grequests.imap([grequests.get(u) for u in urls])]

def kraken(assets):
    pairs = []
    urls = []
    ft = []
    transform = {
        'XBT': 'BTC',
        'XXBT': 'BTC',
        'ZUSD': 'USD',
        'XETH': 'ETH'
        }
    resp = requests.get('https://api.kraken.com/0/public/AssetPairs').json()
    for k, v in resp['result'].items():
        k1 = transform.get(v['base'], v['base'])
        k2 = transform.get(v['quote'], v['quote'])
        if '.d' in k:
            continue
        if k1 in assets and k2 in assets:
            pairs.append(k)
            ft.append([k1, k2])
            urls.append('https://api.kraken.com/0/public/Ticker?pair=%s' % k)
    rs = [grequests.get(u) for u in urls]
    def item(i):
        return {
        'from': i[1][0],
        'to' : i[1][1],
        'bid' : float(i[2][i[0]]['b'][0]),
        'ask' : float(i[2][i[0]]['a'][0]),
        'last' : float(i[2][i[0]]['c'][0])}
        
    return [
        item(i) \
        for i in zip(pairs, ft,
                     [ x.json()['result'] for x in grequests.map(rs)])]

def btcchina(assets):
    urls = []
    pairs = []
    for i in ['ltccny', 'btccny']:
        k1 = i[0:3].upper()
        k2 = i[3:].upper()
        if k1 in assets and k2 in assets:
            pairs.append([k1, k2])
            urls.append('https://data.btcchina.com/data/ticker?market=' + i)
    rs = [grequests.get(u) for u in urls]
    retval = []
    for i in zip(pairs, grequests.map(rs)):
        r = i[1].json()['ticker']
        retval.append({'from':i[0][0],
                       'to':i[0][1],
                       'bid': float(r['buy']),
                       'ask': float(r['sell']),
                       'last': float(r['last'])})
    return retval

def huobi(assets):
    urls = ['http://api.huobi.com/staticmarket/ticker_btc_json.js',
            'http://api.huobi.com/staticmarket/ticker_ltc_json.js',
            'http://api.huobi.com/usdmarket/ticker_btc_json.js',
            'http://be.huobi.com/market/kline?symbol=ethcny&period=1min',
            'http://be.huobi.com/market/depth?symbol=ethcny&type=step1']
    rs = [grequests.get(u) for u in urls]
    rp = [x.json() for x in grequests.map(rs)]
    retval = []
    retval.append({'from': 'BTC',
                   'to': 'CNY',
                   'bid': rp[0]['ticker']['buy'],
                   'ask': rp[0]['ticker']['sell'],
                   'last': rp[0]['ticker']['last']})
    retval.append({'from': 'LTC',
                   'to': 'CNY',
                   'bid': rp[1]['ticker']['buy'],
                   'ask': rp[1]['ticker']['sell'],
                   'last': rp[1]['ticker']['last']})
    retval.append({'from': 'BTC',
                   'to': 'USD',
                   'bid': rp[2]['ticker']['buy'],
                   'ask': rp[2]['ticker']['sell'],
                   'last': rp[2]['ticker']['last']})
    retval.append({'from': 'ETH',
                   'to': 'CNY',
                   'bid': rp[4]['tick']['bids'][0][0],
                   'ask': rp[4]['tick']['asks'][0][0],
                   'last': rp[3]['tick']['close']})
    return retval
                 
#add tag
def add_tag(d, tag):
    d['from'] = d['from'] + ":" + tag
    d['to'] = d['to'] + ":" + tag
    return d
 
tasks = [
    ['btcchina', btcchina],
    ['anx', anx],
    ['bitcashout', bitcashout],
    ['bitfinex', bitfinex],
    ['gatecoin', gatecoin],
    ['poloniex', poloniex],
    ['bitstamp', bitstamp],
    ['kraken', kraken],
    ['huobi', huobi]
    ]

def func(i):
    try:
        return [i[0], i[1](assets)]
    except:
        return [i[0], []]

p = multiprocessing.Pool()
print("#" + time.strftime("%Y-%m-%d %H:%M:%S"))
for k, v in p.imap_unordered(func, tasks):
    for j in v:
        if j['from'] not in assets or j['to'] not in assets:
            continue
        j = add_tag(j,k)
        print(','.join(['bid-ask', j['from'], j['to'], str(j['bid']), str(j['ask']), str(j['last'])]))
