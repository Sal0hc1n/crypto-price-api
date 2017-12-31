import exchanges

print(exchanges.get_exchanges_list())
print(exchanges.get_underlyings_list())
print(exchanges.get_exchanges_list_for_underlying('ETHBTC'))
# exchanges.get_all_quotes(['XRPBTC'])
for en in ['kraken', 'bitfinex', 'bittrex']:
    e = exchanges.get_exchange(en)
    print('== %s ==' % en)
    for u in e.get_supported_underlyings():
        print(u)
        bid = e.get_quote(u, 'bid')
        ask = e.get_quote(u, 'ask')
        print('[%s, %s]' % (bid, ask))
