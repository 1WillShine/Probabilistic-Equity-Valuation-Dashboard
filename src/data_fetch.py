# src/data_fetch.py
import pandas as pd
import yfinance as yf

def fetch_stock(ticker, start, end):
    df = yf.download(
        ticker,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False,
        threads=False
    )

    if df.empty or "Close" not in df.columns:
        return None  # <-- DO NOT RAISE

    out = df[["Close"]].rename(columns={"Close": ticker})
    out.index = pd.to_datetime(out.index)
    return out
