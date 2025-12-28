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

def fit_return_distribution(series):
    mu, sigma = stats.norm.fit(series)
    lam = 1 / np.mean(series[series > 0]) if (series > 0).any() else None

    return {
        "Normal": {"mu": mu, "sigma": sigma},
        "Exponential (positive tail)": {"lambda": lam},
        "Skewness": stats.skew(series),
        "Kurtosis": stats.kurtosis(series)
    }

