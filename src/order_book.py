from typing import Dict, List, Optional, Tuple
from .models import Order, Side, Trade


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
    
    def match(self, order: Order) -> List[Trade]:
        trades: List[Trade] = []

        if order.side == Side.BUY:
            while order.quantity > 0 and self.asks:
                best_ask = self.get_best_ask()
                if best_ask is None:
                    break
                best_price, orders_at_price = best_ask
                if best_price > order.price:
                    break

                best_order = orders_at_price[0]
                traded_qty = min(order.quantity, best_order.quantity)
                trade = Trade(
                    buy_order_id=order.id,
                    sell_order_id=best_order.id,
                    price=best_price,
                    quantity=traded_qty,
                )
                trades.append(trade)

                order.quantity -= traded_qty
                best_order.quantity -= traded_qty

                if best_order.quantity == 0:
                    orders_at_price.pop(0)
                    if not orders_at_price:
                        del self.asks[best_price]

            if order.quantity > 0:
                self.add_order(order)

        else:
            while order.quantity > 0 and self.bids:
                best_bid = self.get_best_bid()
                if best_bid is None:
                    break
                best_price, orders_at_price = best_bid
                if best_price < order.price:
                    break

                best_order = orders_at_price[0]
                traded_qty = min(order.quantity, best_order.quantity)
                trade = Trade(
                    buy_order_id=best_order.id,
                    sell_order_id=order.id,
                    price=best_price,
                    quantity=traded_qty,
                )
                trades.append(trade)

                order.quantity -= traded_qty
                best_order.quantity -= traded_qty

                if best_order.quantity == 0:
                    orders_at_price.pop(0)
                    if not orders_at_price:
                        del self.bids[best_price]

            if order.quantity > 0:
                self.add_order(order)

        return trades

