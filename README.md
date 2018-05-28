Cryptocurrencies Price API
----------------------------------------------------------------------

If you are trying to do interesting things with cryptocurrency price data,
you shouldn't have to be concerned with the low-level details of how
to obtain that data, or the particular JSON structures that it comes in.
This module will provide a unified way of getting price data from various
exchanges which have publicly available API's, as well as a unified
representation of that data rather than exchange specific ones.

### Quick Guide
```python
>>> from exchanges.bitfinex import Bitfinex
>>> Bitfinex().get_quote('BTCUSD', 'bid')
    Decimal('2355.1')
```
        
### Dependencies

The only dependency is on the `requests` library. You can either
do `pip install requests` or `pip install -r requirements.txt` inside the
directory.

### Examples

See test.py for some use cases. Call exchanges.get_exchanges_list() to get a list of supported exchanges.

All of the Exchange classes expose the interface below:
```python
>>> import exchanges
>>> exchanges.get_exchange('gatecoin').get_supported_quotes()
['bid', 'ask', 'last']	
>>> exchanges.get_exchange('gatecoin').get_supported_underlyings()
['BTCUSD', 'BTCEUR', 'ETHBTC']
>>> exchanges.get_exchange('bitstamp').get_quote('BTCUSD', 'ask')
Decimal('2445.05')
```

A simple Telegram bot using this API is also included in example folder
