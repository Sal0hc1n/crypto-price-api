from exchanges import *
import sys

print(get_all_quotes())


"""
def retriever(exchange, currency):
    bid = exchange.get_quote(currency, 'bid')
    sys.stdout.write(exchange.name + ' - ' + currency + ':\n')
    sys.stdout.write('bid: ' + str(bid) + '\n')
    ask = exchange.get_quote(currency, 'ask')
    sys.stdout.write('ask: ' + str(ask) + '\n')
    last = exchange.get_quote(currency, 'last')
    sys.stdout.write('last: ' + str(last) + '\n')
    sys.stdout.write('\n\n')
    sys.stdout.flush()

#bitmex
retriever(BitBay(), 'BTCUSD')
retriever(Bitfinex(), 'BTCUSD')
retriever(BitFlyer(), 'ETHBTC')
retriever(Bitstamp(), 'BTCUSD')
retriever(Bittrex(), 'BTCUSDT')
retriever(Cex(), 'BTCUSD')
#coinbase
price = Coinbase().get_current_price()
print('Coindesk:', str(price))
#CoinDesk
price = CoinDesk().get_current_price()
print('CoinDesk:', str(price))

retriever(GateCoin(), 'BTCUSD')
retriever(GDAX(), 'BTCUSD')
retriever(Gemini(), 'BTCUSD')
retriever(HitBTC(), 'BTCUSD')
retriever(Kraken(), 'BTCUSD')
retriever(OKCoin(), 'BTCUSD')
retriever(Poloniex(), 'BTCUSDT')
"""
