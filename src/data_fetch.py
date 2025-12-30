import yfinance as yf
import pandas as pd

def fetch_prices(tickers, start, end):
    # Ensure tickers is a list, even if a single string is passed
    if isinstance(tickers, str):
        tickers = [tickers]
        
    try:
        data = yf.download(
            tickers=tickers,
            start=start,
            end=end,
            progress=False,
            auto_adjust=True,
            threads=False
        )

        # 1. Handle missing/empty data immediately
        if data is None or data.empty:
            return pd.DataFrame() # Return empty DF instead of None to prevent crashes

        # 2. Extract 'Close' and FORCE into a DataFrame
        if "Close" in data.columns:
            prices = data["Close"]
        else:
            # Fallback if auto_adjust=True changed the name
            prices = data.iloc[:, 0] 

        # 3. Enforcement: Convert Series to DataFrame if necessary
        if isinstance(prices, pd.Series):
            prices = prices.to_frame()
            
        # 4. Standardize column names
        # This ensures your DF always has the tickers as column headers
        prices.columns = tickers

        return prices

    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()



