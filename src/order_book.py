from typing import Dict, List, Optional, Tuple
from .models import Order, Side


class OrderBook:
    def __init__(self):
        self.bids: Dict[float, List[Order]] = {}
        self.asks: Dict[float, List[Order]] = {}

    def add_order(self, order: Order):
        book = self.bids if order.side == Side.BUY else self.asks
        if order.price not in book:
            book[order.price] = []
        book[order.price].append(order)

    def get_best_bid(self) -> Optional[Tuple[float, List[Order]]]:
        if not self.bids:
            return None
        best_price = max(self.bids.keys())
        return best_price, self.bids[best_price]

    def get_best_ask(self) -> Optional[Tuple[float, List[Order]]]:
        if not self.asks:
            return None
        best_price = min(self.asks.keys())
        return best_price, self.asks[best_price]
