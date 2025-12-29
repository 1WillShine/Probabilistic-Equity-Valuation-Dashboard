import numpy as np
import pandas as pd

def time_to_reversion(price, trend):
    """
    Estimate waiting time until price crosses trend again.
    Returns array of durations (days).
    """
    above = price > trend
    switches = above.ne(above.shift()).cumsum()
    durations = switches.value_counts().values
    return durations


def fit_exponential_waiting_time(durations):
    """
    Fit exponential distribution to waiting times.
    """
    durations = np.array(durations)
    lambda_hat = 1.0 / durations.mean()
    return lambda_hat
import numpy as np
from scipy import stats

import numpy as np
import pandas as pd
from scipy import stats

def fit_return_distribution(series: pd.Series) -> dict:
    """
    Fit parametric distributions to return series.
    Robust to NaNs, infs, and short samples.
    """

    # --------------------------------------------------
    # Sanitize data
    # --------------------------------------------------
    clean = (
        series
        .replace([np.inf, -np.inf], np.nan)
        .dropna()
    )

    # Guard: insufficient data
    if len(clean) < 30:
        return {
            "status": "insufficient_data",
            "n_obs": len(clean)
        }

    results = {
        "n_obs": len(clean)
    }

    # --------------------------------------------------
    # Normal distribution
    # --------------------------------------------------
    mu, sigma = stats.norm.fit(clean)

    results["normal"] = {
        "mu": float(mu),
        "sigma": float(sigma),
        "skew": float(stats.skew(clean)),
        "kurtosis": float(stats.kurtosis(clean))
    }

    # --------------------------------------------------
    # Student-t distribution (fat tails)
    # --------------------------------------------------
    try:
        df, loc, scale = stats.t.fit(clean)
        results["student_t"] = {
            "df": float(df),
            "loc": float(loc),
            "scale": float(scale)
        }
    except Exception:
        results["student_t"] = "fit_failed"

    # --------------------------------------------------
    # Jarque–Bera normality test
    # --------------------------------------------------
    jb_stat, jb_p = stats.jarque_bera(clean)
    results["jarque_bera_p"] = float(jb_p)

    return results


