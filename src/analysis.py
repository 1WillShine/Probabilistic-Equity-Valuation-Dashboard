# src/analysis.py
import numpy as np
import pandas as pd

# -----------------------------------------------------------
# 1. LOG TREND (log-price regression) 
# -----------------------------------------------------------
def compute_log_trend(series: pd.Series):
    """
    Fit log(price) ~ time to produce an exponential/trend line.
    Returns a pandas Series aligned with the original index.
    """
    series = series.dropna()
    y = np.log(series.values)
    x = np.arange(len(series))

    # Linear regression in log-space
    coef = np.polyfit(x, y, 1)
    trend_log = np.polyval(coef, x)
    trend = np.exp(trend_log)

    trend_series = pd.Series(trend, index=series.index, name="log_trend")
    return trend_series


# -----------------------------------------------------------
# 2. SMOOTH TREND (moving average)
# -----------------------------------------------------------
def compute_smooth_trend(series: pd.Series, window=50):
    """
    Returns a simple moving average to smooth volatility.
    """
    return series.rolling(window=window, min_periods=1).mean()


# -----------------------------------------------------------
# 3. % DISTANCE FROM TREND
# -----------------------------------------------------------
def pct_distance(series: pd.Series, trend: pd.Series):
    """
    Computes (price - trend) / trend as percent distance.
    """
    return (series - trend) / trend * 100.0

import numpy as np
import pandas as pd

def compute_returns(price_df):
    return price_df.pct_change().dropna()

import pandas as pd

def portfolio_returns(returns: pd.DataFrame, weights) -> pd.Series:
    """
    Compute portfolio returns with strict alignment.
    """
    # Convert weights to Series if needed
    if not isinstance(weights, pd.Series):
        weights = pd.Series(weights, index=returns.columns)

    # Reindex to guarantee alignment
    weights = weights.reindex(returns.columns)

    # Normalize weights defensively
    weights = weights / weights.sum()

    return returns.dot(weights)


def rolling_sharpe(returns, rf_rate, window):
    daily_rf = rf_rate / 252
    excess = returns - daily_rf
    return (
        excess.rolling(window).mean()
        / excess.rolling(window).std()
        * np.sqrt(252)
    )

import pandas as pd
import numpy as np

def regime_conditioned_sharpe(
    returns: pd.Series,
    rf_rate: float = 0.0,
    vol_window: int = 21
) -> pd.Series:
    """
    Compute Sharpe ratios conditioned on volatility regimes.
    Robust to flat or low-variance volatility series.
    """

    # Rolling volatility
    vol = returns.rolling(vol_window).std().dropna()

    # Guard: not enough data
    if vol.nunique() < 3:
        return pd.Series(
            {
                "Low Vol": np.nan,
                "Mid Vol": np.nan,
                "High Vol": np.nan,
            }
        )

    # Quantile binning with duplicate handling
    regimes = pd.qcut(
        vol,
        q=3,
        labels=["Low Vol", "Mid Vol", "High Vol"],
        duplicates="drop"
    )

    sharpe_by_regime = {}

    aligned_returns = returns.loc[vol.index]

    for regime in regimes.cat.categories:
        mask = regimes == regime
        r = aligned_returns[mask]

        if r.std() == 0 or len(r) < 5:
            sharpe_by_regime[regime] = np.nan
        else:
            sharpe_by_regime[regime] = (
                (r.mean() - rf_rate / 252) / r.std()
            ) * np.sqrt(252)

    return pd.Series(sharpe_by_regime)





