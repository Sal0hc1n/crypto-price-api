from exchanges.bitfinex import Bitfinex
from exchanges.bitstamp import Bitstamp
from exchanges.bitvc import BitVc
from exchanges.coinapult import Coinapult
from exchanges.coindesk import CoinDesk
from exchanges.futures796 import Futures796
from exchanges.huobi import Huobi
from exchanges.kraken import Kraken
from exchanges.okcoin import OKCoin, OKCoinFutures
from exchanges.poloniex import Poloniex
from exchanges.bravenewcoin import BraveNewCoin
from exchanges.gatecoin import GateCoin
from exchanges.cexio import CexIO
from exchanges.bitbay import BitBay
from exchanges.hitbtc import HitBTC

exchange_list = {
    'bitfinex' : Bitfinex,
    'bitstamp' : Bitstamp,
    'bitbay' : BitBay,
#    'bitvc' : BitVc,
    'cex.io' : CexIO,
    'coinapult' : Coinapult,
#    'coindesk' : CoinDesk,
#    'futures796' : Futures796,
#    'huobi' : Huobi,
    'hitbtc' : HitBTC,
    'kraken' : Kraken,
    'okcoin' : OKCoin,
#    'okcoin_futures' : OKCoinFutures,
    'poloniex' : Poloniex,
#    'bravenewcoin' : BraveNewCoin,
    'gatecoin' : GateCoin
}

def get_exchange(s, *args, **kwargs):
    if s not in exchange_list:
        raise RuntimeError
    else:
        return exchange_list[s](*args, **kwargs)
