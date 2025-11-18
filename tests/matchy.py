from src.order_book import OrderBook
from src.models import Order, Side, OrderType, TimeInForce


def test_full_match_buy_hits_existing_sell():
    ob = OrderBook()
    sell = Order(1, Side.SELL, 100, 5)
    ob.add_order(sell)

    buy = Order(2, Side.BUY, 105, 5)
    trades = ob.match(buy)

    assert len(trades) == 1
    t = trades[0]
    assert t.price == 100
    assert t.quantity == 5
    assert t.buy_order_id == 2
    assert t.sell_order_id == 1
    assert ob.get_best_ask() is None


def test_partial_fill_incoming_buy():
    ob = OrderBook()
    sell = Order(1, Side.SELL, 100, 3)
    ob.add_order(sell)

    buy = Order(2, Side.BUY, 100, 5)
    trades = ob.match(buy)

    assert len(trades) == 1
    t = trades[0]
    assert t.quantity == 3
    best_bid = ob.get_best_bid()
    assert best_bid is not None
    best_price, orders = best_bid
    assert best_price == 100
    assert len(orders) == 1
    assert orders[0].quantity == 2
    assert orders[0].id == 2


def test_partial_fill_incoming_sell():
    ob = OrderBook()
    buy = Order(1, Side.BUY, 100, 4)
    ob.add_order(buy)

    sell = Order(2, Side.SELL, 95, 2)
    trades = ob.match(sell)

    assert len(trades) == 1
    t = trades[0]
    assert t.quantity == 2
    best_bid = ob.get_best_bid()
    assert best_bid is not None
    _, orders = best_bid
    assert orders[0].quantity == 2


def test_no_match_buy_too_low():
    ob = OrderBook()
    sell = Order(1, Side.SELL, 110, 5)
    ob.add_order(sell)

    buy = Order(2, Side.BUY, 100, 5)
    trades = ob.match(buy)

    assert trades == []
    best_bid = ob.get_best_bid()
    assert best_bid is not None
    best_price, orders = best_bid
    assert best_price == 100
    assert len(orders) == 1
    assert orders[0].id == 2
    best_ask = ob.get_best_ask()
    assert best_ask is not None
    assert best_ask[0] == 110


def test_multiple_price_levels_match_in_order():
    ob = OrderBook()
    ob.add_order(Order(1, Side.SELL, 95, 2))
    ob.add_order(Order(2, Side.SELL, 97, 3))
    ob.add_order(Order(3, Side.SELL, 100, 4))

    buy = Order(4, Side.BUY, 100, 7)
    trades = ob.match(buy)

    assert len(trades) == 3
    assert trades[0].price == 95
    assert trades[0].quantity == 2
    assert trades[1].price == 97
    assert trades[1].quantity == 3
    assert trades[2].price == 100
    assert trades[2].quantity == 2

    best_ask = ob.get_best_ask()
    assert best_ask is not None
    price, orders = best_ask
    assert price == 100
    assert len(orders) == 1
    assert orders[0].quantity == 2

def test_market_buy_ignores_price():
    ob = OrderBook()
    ob.add_order(Order(id=1, side=Side.SELL, price=100, quantity=5))

    buy = Order(
        id=2,
        side=Side.BUY,
        price=0,
        quantity=5,
        order_type=OrderType.MARKET,
    )
    trades = ob.match(buy)

    assert len(trades) == 1
    t = trades[0]
    assert t.price == 100
    assert t.quantity == 5
    assert ob.get_best_ask() is None


def test_ioc_does_not_rest_in_book():
    ob = OrderBook()
    ob.add_order(Order(id=1, side=Side.SELL, price=100, quantity=2))

    buy = Order(
        id=2,
        side=Side.BUY,
        price=100,
        quantity=5,
        order_type=OrderType.LIMIT,
        time_in_force=TimeInForce.IOC,
    )
    trades = ob.match(buy)

    assert len(trades) == 1
    t = trades[0]
    assert t.quantity == 2

    best_bid = ob.get_best_bid()
    assert best_bid is None
