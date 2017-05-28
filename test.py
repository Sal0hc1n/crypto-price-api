import exchanges
print(exchanges.get_exchanges_list())
print(exchanges.get_underlyings_list())
print(exchanges.get_exchanges_list_for_underlying('ETHBTC'))
exchanges.get_all_quotes(['XRPBTC'])
