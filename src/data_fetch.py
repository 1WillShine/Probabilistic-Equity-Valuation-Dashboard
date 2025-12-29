# src/data_fetch.py
import yfinance as yf
import pandas as pd

def fetch_prices(tickers, start, end):
    """
    Batch fetch prices to avoid Yahoo rate limits.
    Returns Close prices DataFrame.
    """
    try:
        data = yf.download(
            tickers=tickers,
            start=start,
            end=end,
            progress=False,
            auto_adjust=True,
            threads=False
        )

        if data.empty:
            return None

        # Handle multi-index columns
        if isinstance(data.columns, pd.MultiIndex):
            prices = data["Close"]
        else:
            prices = data[["Close"]]
            prices.columns = tickers

        return prices

    except Exception as e:
        return None


