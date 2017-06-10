import exchanges
import sys
import requests

# get API key from https://currencylayer.com/
CL_API_KEY = 'APIKEY'

if len(sys.argv) <= 1:
    FXPAIR = 'USDHKD'
else:
    FXPAIR = sys.argv[1]

if len(sys.argv) <=2:
    size = 1
else:
    size = int(sys.argv[2])

FORCCY = FXPAIR[:3].upper()
DOMCCY = FXPAIR[-3:].upper()

FORPAIR = 'BTC'+FORCCY
DOMPAIR = 'BTC'+DOMCCY

forExchanges = exchanges.get_exchanges_list_for_underlying(FORPAIR)
domExchanges = exchanges.get_exchanges_list_for_underlying(DOMPAIR)

intersectExchanges = list(set(forExchanges).intersection(domExchanges))

url = 'http://www.apilayer.net/api/live?access_key='+CL_API_KEY+'&currencies='+FORCCY+','+DOMCCY

r = requests.get(url)
r.raise_for_status()
j = r.json()
if j['success']:
    domOfficialRate = r.json()['quotes']['USD'+DOMCCY]
    forOfficialRate = r.json()['quotes']['USD'+FORCCY]
    fxRate = domOfficialRate / forOfficialRate
    print('Currency Layer %s FX rate is %.5g' % (FXPAIR, fxRate))
else:
    fxRate = 0
    print('Could not retrieve %s FX rate from CurrencyLayer' % FXPAIR)

for exch in intersectExchanges:
    e = exchanges.get_exchange(exch)
    sizeSuccess = False
    try:
        domDepth = e.get_depth(DOMPAIR,size)
        forDepth = e.get_depth(FORPAIR,size)
        fx_bid = domDepth[0] / forDepth[1]
        fx_ask = domDepth[1] / forDepth[0]
        sizeSuccess = True
    except:
        print('Depth failed, trying just regular bid')
        try:
            fx_bid = e.get_quote(DOMPAIR,'bid') / e.get_quote(FORPAIR,'ask')
            fx_ask = e.get_quote(DOMPAIR,'ask') / e.get_quote(FORPAIR,'bid')
        except ZeroDivisionError:
            print('%s: one of the quotes is worth 0' % exch)
            continue
    if fxRate != 0 and (fx_bid > fxRate or fx_ask < fxRate):
        if fx_bid > fxRate:
            arb = 100 * (float(fx_bid) / fxRate - 1)
            if sizeSuccess:
                executableSize = min(domDepth[2],forDepth[3])
        else:
            arb = 100 * (fxRate / float(fx_ask) - 1)
            if sizeSuccess:
                executableSize = min(domDepth[3],forDepth[2])
        if sizeSuccess:
            print('%s on %s: bid %.5g / %.5g ask. %.2f%% arb vs %.5g official rate for %s BTC' % (FXPAIR, exch, fx_bid, fx_ask, arb, fxRate, executableSize))
        else:
            print('%s on %s: bid %.5g / %.5g ask. %.2f%% arb vs %.5g official rate' % (FXPAIR, exch, fx_bid, fx_ask, arb, fxRate))
    else:
        print('%s on %s: bid %.5g / %.5g ask' % (FXPAIR, exch, fx_bid, fx_ask))
