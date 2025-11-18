from src.order_book import OrderBook
from src.models import Order, Side


def test_add_buy_orders():
    ob = OrderBook()
    o1 = Order(1, Side.BUY, 100, 5)
    o2 = Order(2, Side.BUY, 105, 3)

    ob.add_order(o1)
    ob.add_order(o2)

    best = ob.get_best_bid()
    assert best[0] == 105
    assert len(best[1]) == 1


def test_add_sell_orders():
    ob = OrderBook()
    o1 = Order(1, Side.SELL, 200, 5)
    o2 = Order(2, Side.SELL, 190, 3)

    ob.add_order(o1)
    ob.add_order(o2)

    best = ob.get_best_ask()
    assert best[0] == 190
    assert len(best[1]) == 1


def test_empty_book():
    ob = OrderBook()
    assert ob.get_best_bid() is None
    assert ob.get_best_ask() is None
def test_cancel_existing_order():
    ob = OrderBook()
    o1 = Order(1, Side.BUY, 100, 5)
    o2 = Order(2, Side.BUY, 99, 3)
    ob.add_order(o1)
    ob.add_order(o2)

    ok = ob.cancel_order(1)
    assert ok is True

    best = ob.get_best_bid()
    assert best is not None
    price, orders = best
    assert price == 99
    assert len(orders) == 1
    assert orders[0].id == 2


def test_cancel():
    ob = OrderBook()
    o1 = Order(1, Side.SELL, 110, 4)
    ob.add_order(o1)

    ok = ob.cancel_order(999)
    assert ok is False

    best = ob.get_best_ask()
    assert best is not None
    price, orders = best
    assert price == 110
    assert len(orders) == 1
