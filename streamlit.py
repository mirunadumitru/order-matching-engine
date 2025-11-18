import streamlit as st
from src.exchange import Exchange
from src.models import Side, OrderType, TimeInForce


def get_exchange():
    if "exchange" not in st.session_state:
        st.session_state.exchange = Exchange()
    return st.session_state.exchange


def get_trades_history():
    if "trades_history" not in st.session_state:
        st.session_state.trades_history = []
    return st.session_state.trades_history


st.set_page_config(page_title="Order Matching Engine", layout="wide")

st.title("Order Matching Engine Demo")

ex = get_exchange()
trades_history = get_trades_history()

col1, col2 = st.columns(2)

with col1:
    st.subheader("New Order")

    side_str = st.selectbox("Side", ["BUY", "SELL"])
    side = Side.BUY if side_str == "BUY" else Side.SELL

    order_type_str = st.selectbox("Order Type", ["LIMIT", "MARKET"])
    order_type = OrderType.LIMIT if order_type_str == "LIMIT" else OrderType.MARKET

    tif_str = st.selectbox("Time In Force", ["GTC", "IOC"])
    time_in_force = TimeInForce.GTC if tif_str == "GTC" else TimeInForce.IOC

    if order_type == OrderType.LIMIT:
        price = st.number_input("Price", min_value=0.0, value=100.0, step=1.0)
    else:
        st.info("Market order: price is ignored and will hit best available prices.")
        price = 0.0

    quantity = st.number_input("Quantity", min_value=1, value=5, step=1)

    if st.button("Submit Order"):
        trades = ex.submit_order(
            side=side,
            price=price,
            quantity=int(quantity),
            order_type=order_type,
            time_in_force=time_in_force,
        )
        for t in trades:
            trades_history.append(
                {
                    "buy_order_id": t.buy_order_id,
                    "sell_order_id": t.sell_order_id,
                    "price": t.price,
                    "quantity": t.quantity,
                    "timestamp": t.timestamp,
                }
            )
        st.success(f"Submitted {side_str} {order_type_str} x{int(quantity)}")


with col2:
    st.subheader("Best Bid / Ask")
    best_bid = ex.get_best_bid()
    best_ask = ex.get_best_ask()

    bb_text = f"{best_bid[0]} (qty {best_bid[1]})" if best_bid else "None"
    ba_text = f"{best_ask[0]} (qty {best_ask[1]})" if best_ask else "None"

    st.write(f"**Best Bid:** {bb_text}")
    st.write(f"**Best Ask:** {ba_text}")

st.markdown("---")

snapshot = ex.get_order_book_snapshot()
bids = snapshot["bids"]
asks = snapshot["asks"]

col_bids, col_asks = st.columns(2)

with col_bids:
    st.subheader("Bids")
    if bids:
        bid_rows = [
            {"price": p, "quantity": q} for p, q in sorted(bids.items(), key=lambda x: -x[0])
        ]
        st.table(bid_rows)
    else:
        st.write("No bids")

with col_asks:
    st.subheader("Asks")
    if asks:
        ask_rows = [
            {"price": p, "quantity": q} for p, q in sorted(asks.items(), key=lambda x: x[0])
        ]
        st.table(ask_rows)
    else:
        st.write("No asks")

st.markdown("---")

st.subheader("Trade History")

if trades_history:
    st.dataframe(trades_history)
else:
    st.write("No trades yet")
