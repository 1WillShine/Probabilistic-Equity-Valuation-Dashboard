import numpy as np
import pandas as pd

def bootstrap_sharpe(returns, n_boot=2000, rf=0.0):
    """
    Bootstrap Sharpe ratio confidence intervals.

    Parameters
    ----------
    returns : pd.Series
        Daily return series
    n_boot : int
        Number of bootstrap samples
    rf : float
        Risk-free rate (daily)

    Returns
    -------
    dict with mean, lower, upper
    """
    returns = returns.dropna().values
    sharpe_samples = []

    for _ in range(n_boot):
        sample = np.random.choice(returns, size=len(returns), replace=True)
        mu = sample.mean() - rf
        sigma = sample.std(ddof=1)
        if sigma > 0:
            sharpe_samples.append(mu / sigma)

    sharpe_samples = np.array(sharpe_samples)

    return {
        "mean": sharpe_samples.mean(),
        "lower": np.percentile(sharpe_samples, 5),
        "upper": np.percentile(sharpe_samples, 95)
    }
    import numpy as np

def bootstrap_ci(series, n=5000, alpha=0.05):
    means = []
    arr = series.values

    for _ in range(n):
        sample = np.random.choice(arr, size=len(arr), replace=True)
        means.append(sample.mean())

    low = np.percentile(means, 100 * alpha / 2)
    high = np.percentile(means, 100 * (1 - alpha / 2))
    return low, high
# src/visualization.py
import plotly.graph_objects as go

def animated_ci_band(ci_df):
    """
    Animated rolling CI band for mean returns.
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=ci_df.index,
        y=ci_df["upper"],
        line=dict(width=0),
        showlegend=False,
        hoverinfo="skip"
    ))

    fig.add_trace(go.Scatter(
        x=ci_df.index,
        y=ci_df["lower"],
        fill="tonexty",
        fillcolor="rgba(0, 100, 255, 0.2)",
        line=dict(width=0),
        name="95% CI"
    ))

    fig.add_trace(go.Scatter(
        x=ci_df.index,
        y=ci_df["mean"],
        line=dict(color="blue", width=2),
        name="Rolling Mean"
    ))

    fig.update_layout(
        title="Rolling Mean Return with Bootstrap CI",
        xaxis_title="Date",
        yaxis_title="Mean Return",
        height=450
    )
def rolling_bootstrap_ci(series, window=126, n_boot=1000, alpha=0.05):
    """
    Rolling bootstrap confidence intervals for mean return.
    """
    results = []

    for i in range(window, len(series)):
        sample = series.iloc[i - window:i]
        boot_means = np.random.choice(sample, (n_boot, len(sample)), replace=True).mean(axis=1)

        results.append({
            "date": series.index[i],
            "mean": sample.mean(),
            "lower": np.percentile(boot_means, 100 * alpha / 2),
            "upper": np.percentile(boot_means, 100 * (1 - alpha / 2)),
        })

    return pd.DataFrame(results).set_index("date")

    return fig


