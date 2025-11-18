from dataclasses import dataclass
from enum import Enum
from typing import Optional
import time


class Side(Enum):
    BUY = "BUY"
    SELL = "SELL"


@dataclass
class Order:
    id: int
    side: Side
    price: float
    quantity: int
    timestamp: Optional[float] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()
        if self.price <= 0:
            raise ValueError("lower than 0 error")
        if self.quantity <= 0:
            raise ValueError("lower than 0 error")


@dataclass
class Trade:
    buy_order_id: int
    sell_order_id: int
    price: float
    quantity: int
    timestamp: Optional[float] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()
        if self.price <= 0:
            raise ValueError("lower than 0 error")
        if self.quantity <= 0:
            raise ValueError("lower than 0 error")
