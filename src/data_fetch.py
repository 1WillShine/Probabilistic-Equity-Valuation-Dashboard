# src/data_fetch.py
import yfinance as yf
import pandas as pd

def fetch_stock(ticker: str, start, end):
    df = yf.download(
        ticker,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False
    )

    # ❌ No data
    if df is None or df.empty:
        return None

    # 🔹 Case 1: MultiIndex columns (rare but deadly)
    if isinstance(df.columns, pd.MultiIndex):
        if "Close" in df.columns.get_level_values(0):
            df = df["Close"]
        else:
            return None

    # 🔹 Case 2: DataFrame with Close column
    if isinstance(df, pd.DataFrame):
        if "Close" not in df.columns:
            return None
        prices = df["Close"]

    # 🔹 Case 3: Series already
    elif isinstance(df, pd.Series):
        prices = df

    else:
        return None

    # 🔹 Final normalization
    prices = prices.dropna()
    prices.name = ticker

    return prices.to_frame()
