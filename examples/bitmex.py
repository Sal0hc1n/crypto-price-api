from exchanges.bitmex import BitMEX

e = bitMEX
spot_sym = 'XBTUSD'
fut_sym = 'XBTH18'
e.init_symbol(spot_sym)
e.init_symbol(fut_sym)
spot_bid = e.get_quote(spot_sym, 'bid')
fut_bid = e.get_quote(fut_sym, 'bid')
spot_ask = e.get_quote(spot_sym, 'ask')
fut_ask = e.get_quote(fut_sym, 'ask')
basis = [fut_bid - spot_ask,fut_ask - spot_bid]
print(e.get_instrument(fut_sym))
print(basis)
print(e.get_balance())
