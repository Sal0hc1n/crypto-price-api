Crypto Price API
----------------------------------------------------------------------
![status](https://img.shields.io/badge/Status-Testing-yellow.svg)
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

### Exchanges

The curret exchanges api supported are:
- [bitbay](https://bitbay.net/en)
- [bitfinex](https://www.bitfinex.com/)
- [bitflyer](https://bitflyer.com/en-us/)
- [bitmex](https://www.bitmex.com/)
- [bitstamp](https://www.bitstamp.net/)
- [bittrex](https://bittrex.com/)
- [cex](https://cex.io/)
- [coinbase](https://www.coinbase.com/)
- [gatecoin](https://gatecoin.com/)
- [gdax](https://www.gdax.com/)
- [gemin](https://gemini.com/)
- [hitbtc](https://hitbtc.com/)
- [kraken](https://www.kraken.com/)
- [liqui](https://liqui.io/)
- [okcoin](https://www.okcoin.com/)
- [poloniex](https://poloniex.com/) [API]()

### Coindesk api

The [coindesk](https://www.coindesk.com/api/) class offers a much richer price interface:
```Python
get_current_price(currency='USD')
get_past_price(date)
get_historical_data_as_dict(start='2013-09-01', end=None)
get_historical_data_as_list(start='2013-09-01', end=None)
```

`get_current_price` and `get_past_price` both return `Decimal` objects.

`get_current_price` takes in an optional parameter specifying the currency.

The dates for all functions must be in the form 'YYYY-MM-DD'.

`get_historical_data_as_dict` will return a dictionary of the following format:

```Python
    {'2014-10-20': 400.00, '2014-10-21': 301.99}
```
Remember that these date/prices will not be in any given order.

`get_historical_data_as_list` will return a list of dictionaries, correctly
sorted by date from start to end.

```Python
    [
        {'date': 'YYYY-MM-DD', 'price': 300.00},
        {'date': 'YYYY-MM-DD', 'price': 301.00 }
    ]
```

### Examples

See test.py for some use cases. Call ```exchanges.get_exchanges_list()``` to get a list of supported exchanges.

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

### Note

This repo it's the result of collective effords, and it aims to bring a universal api wrap of various exchange
