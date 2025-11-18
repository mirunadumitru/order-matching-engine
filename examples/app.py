from src.exchange import Exchange
from src.models import Side


def main():
    ex = Exchange()

    print("Submitting some orders")

    ex.submit_order(Side.BUY, 100, 5)
    ex.submit_order(Side.BUY, 99, 3)
    ex.submit_order(Side.SELL, 105, 4)

    print("Best bid:", ex.get_best_bid())
    print("Best ask:", ex.get_best_ask())

    print("\nNow giving a buy that should match:")
    trades = ex.submit_order(Side.BUY, 105, 4)

    for t in trades:
        print(
            f"Trade: buy_id={t.buy_order_id}, sell_id={t.sell_order_id}, "
            f"price={t.price}, qty={t.quantity}"
        )

    print("\nOrder book snapshot:")
    snapshot = ex.get_order_book_snapshot()
    print("Bids:", snapshot["bids"])
    print("Asks:", snapshot["asks"])


if __name__ == "__main__":
    main()
