Cryptocurrencies Price API
----------------------------------------------------------------------

If you are trying to do interesting things with cryptocurrency price data,
you shouldn't have to be concerned with the low-level details of how
to obtain that data, or the particular JSON structures that it comes in.
This module will provide a unified way of getting price data from various
exchanges which have publicly available API's, as well as a unified
representation of that data rather than exchange specific ones.

### Quick Guide

        >>> from exchanges.bitfinex import Bitfinex
        >>> Bitfinex().get_current_price('BTCUSD')
        Decimal('371.17')

### Dependencies

The only dependency is on the `requests` library. You can either
do `pip install requests` or `pip install -r requirements.txt` inside the
directory.

### Various exchanges

See test.py for some use cases. Call exchanges.get_exchanges_list() to get a list of supported exchanges.

All of these classes expose the interface below:

    get_supported_quotes() # returns ['bid', 'ask', 'last'] currently. all exchange classes implement these 3 quotes    
    get_supported_underlyings() # returns a list of currency pairs supported in each exchange class    
    get_quote('BTCUSD', 'bid') # returns the btcusd bid on current exchange
    It will return a `Decimal` object.

