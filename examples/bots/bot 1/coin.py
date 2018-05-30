from exchanges.coinapult import Coinapult


def get_current_value():
    return float(Coinapult().get_current_price())
