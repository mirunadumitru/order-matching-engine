# Order Matching Engine

This project is a basic order matching engine written in Python.
It keeps track of buy and sell orders using a simple limit order book.
It supports limit orders, market orders, and IOC orders.
I also created a Streamlit interface so you can interact with the engine through a web page and see the order book and trades update.

The purpose of this project was to learn how a matching engine works and to practice writing code with tests and a small user interface.

## Features

- Buy and sell limit orders
- Market orders that ignore price
- IOC orders (immediate or cancel)
- Price-time priority matching
- FIFO inside each price level
- Order cancelling
- Streamlit interface for submitting orders
- Test suite using pytest

## Running Tests

    pytest -q

## Running the Streamlit App

    streamlit run streamlit.py

This will open a web page where you can:

- Choose buy or sell
- Select order type (limit or market)
- Select time in force (GTC or IOC)
- Enter price and quantity
- Submit orders
- View the best bid and best ask
- View the order book
- See trade history

## How Matching Works

- A buy order matches with the lowest sell prices.
- A sell order matches with the highest buy prices.
- Limit orders only match when prices cross.
- Market orders match immediately.
- IOC orders do not rest in the book.
- The remaining part of normal limit orders stays in the book.

## Example

There is a small example script in examples/simple_simulation.py.
You can run it with:
    python -m examples.app
