Bitcoin Price API
----------------------------------------------------------------------

If you are trying to do interesting things with bitcoin price data,
you shouldn't have to be concerned with the low-level details of how
to obtain that data, or the particular JSON structures that it comes in.
This module will provide a unified way of getting price data from various
exchanges which have publicly available API's, as well as a unified
representation of that data rather than exchange specific ones.

### Quick Guide

        >>> from exchanges.bitfinex import Bitfinex
        >>> Bitfinex().get_current_price()
        Decimal('371.17')

### Dependencies

The only dependency is on the `requests` library. You can either
do `pip install requests` or `pip install -r requirements.txt` inside the
directory.

### Various exchanges

See test.py for some use cases. Call exchanges.get_exchanges_list() to get a list of supported exchanges.

All of these classes expose the interface below:

    get_last_price('BTCUSD')
    get_current_bid('BTCUSD')
    get_current_ask('BTCUSD')

which will return a `Decimal` object.

The list of underlyings that an exchange supports can be called from exchanges.get_exchange('gatecoin').get_supported_underlyings()
