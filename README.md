Crypto Price API
----------------------------------------------------------------------
![status](https://img.shields.io/badge/Status-Testing-yellow.svg)
[![Python](https://img.shields.io/badge/python-powered-blue.svg)](https://www.python.org/) </br>
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

| #  | Exchange                                | API     |
|----|-----------------------------------------|---------|
| 01 | [bitbay](https://bitbay.net/en)         | [API]() |
| 02 | [bitfinex](https://www.bitfinex.com/)   | [API]() |
| 03 | [bitflyer](https://bitflyer.com/en-us/) | [API]() |
| 04 | [bitmex](https://www.bitmex.com/)       | [API]() |
| 05 | [bitstamp](https://www.bitstamp.net/)   | [API]() |
| 06 | [bittrex](https://bittrex.com/)         | [API]() |
| 07 | [cex](https://cex.io/)                  | [API]() |
| 08 | [coinbase](https://www.coinbase.com/)   | [API]() |
| 09 | [gdax](https://www.gdax.com/)           | [API]() |
| 10 | [gemin](https://gemini.com/)            | [API]() |
| 11 | [hitbtc](https://hitbtc.com/)           | [API]() |
| 12 | [kraken](https://www.kraken.com/)       | [API]() | 
| 13 | [okcoin](https://www.okcoin.com/)       | [API]() |
| 14 | [poloniex](https://poloniex.com/)       | [API]() |

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
