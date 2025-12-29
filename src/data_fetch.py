# src/data_fetch.py
import yfinance as yf
import pandas as pd

def fetch_stock(ticker, start, end):
    df = yf.download(
        ticker,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False,
        group_by="column"
    )

    if df.empty:
        return None

    # Handle MultiIndex edge-case
    if isinstance(df.columns, pd.MultiIndex):
        df = df["Close"]

    if "Close" not in df.columns and df.name != "Close":
        return None

    prices = df["Close"] if "Close" in df.columns else df
    prices = prices.rename(ticker).to_frame()

    prices.index = pd.to_datetime(prices.index)
    return prices


