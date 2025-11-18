from src.exchange import Exchange
from src.models import Side


def test_simple_exchange_flow():
    ex = Exchange()

    ex.submit_order(Side.BUY, 100, 5)
    ex.submit_order(Side.SELL, 105, 3)

    best_bid = ex.get_best_bid()
    best_ask = ex.get_best_ask()

    assert best_bid is not None
    assert best_ask is not None
    assert best_bid[0] == 100
    assert best_ask[0] == 105


def test_exchange_matching():
    ex = Exchange()

    ex.submit_order(Side.SELL, 100, 5)
    trades = ex.submit_order(Side.BUY, 105, 5)

    assert len(trades) == 1
    t = trades[0]
    assert t.price == 100
    assert t.quantity == 5
    assert ex.get_best_bid() is None
    assert ex.get_best_ask() is None
