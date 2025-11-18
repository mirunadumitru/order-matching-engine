from typing import List, Optional, Tuple
from .models import Order, Trade, Side, OrderType, TimeInForce
from .order_book import OrderBook


class Exchange:
    def __init__(self):
        self.order_book = OrderBook()
        self.next_order_id = 1

    def _get_next_id(self) -> int:
        i = self.next_order_id
        self.next_order_id += 1
        return i

    def submit_order(
        self,
        side: Side,
        price: float,
        quantity: int,
        order_type: OrderType = OrderType.LIMIT,
        time_in_force: TimeInForce = TimeInForce.GTC,
    ) -> List[Trade]:
        order = Order(
            id=self._get_next_id(),
            side=side,
            price=price,
            quantity=quantity,
            order_type=order_type,
            time_in_force=time_in_force,
        )
        trades = self.order_book.match(order)
        return trades


    def get_best_bid(self) -> Optional[Tuple[float, int]]:
        best = self.order_book.get_best_bid()
        if best is None:
            return None
        price, orders = best
        total = sum(o.quantity for o in orders)
        return price, total

    def get_best_ask(self) -> Optional[Tuple[float, int]]:
        best = self.order_book.get_best_ask()
        if best is None:
            return None
        price, orders = best
        total = sum(o.quantity for o in orders)
        return price, total

    def get_order_book_snapshot(self):
        bids = {}
        for price, orders in self.order_book.bids.items():
            bids[price] = sum(o.quantity for o in orders)

        asks = {}
        for price, orders in self.order_book.asks.items():
            asks[price] = sum(o.quantity for o in orders)

        return {"bids": bids, "asks": asks}
