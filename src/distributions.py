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
