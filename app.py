import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta

from src.data_fetch import fetch_stock
from src.analysis import (
    compute_returns,
    portfolio_returns,
    rolling_sharpe,
    regime_conditioned_sharpe
)
from src.bootstrap import bootstrap_ci
from src.distributions import fit_return_distribution

st.set_page_config(layout="wide", page_title="Probabilistic Equity Valuation")

st.title("📈 Probabilistic Equity Valuation Dashboard")

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Portfolio Construction")
    tickers = st.text_input("Tickers (comma separated)", "AAPL,MSFT,GOOGL")
    weights = st.text_input("Weights (comma separated)", "0.4,0.3,0.3")

    start_date = st.date_input("Start Date", date.today() - timedelta(days=365 * 3))
    end_date = st.date_input("End Date", date.today())

    st.divider()
    st.header("Risk Settings")
    rf_rate = st.number_input("Risk-Free Rate (annual)", value=0.03, step=0.005)
    window = st.slider("Rolling Window (days)", 30, 252, 126)

tickers = [t.strip().upper() for t in tickers.split(",")]
weights = [float(w) for w in weights.split(",")]

if len(tickers) != len(weights):
    st.error("Tickers and weights must have same length.")
    st.stop()

weights = pd.Series(weights, index=tickers)
weights /= weights.sum()

# ---------------- Data Fetch ----------------
@st.cache_data(ttl=3600)
def load_prices(tickers, start, end):
    dfs = []
    for t in tickers:
        df = fetch_stock(t, start, end)
        dfs.append(df.rename(columns={t: t}))
    return pd.concat(dfs, axis=1).dropna()

prices = load_prices(tickers, start_date, end_date)

returns = compute_returns(prices)
port_ret = portfolio_returns(returns, weights)

# ---------------- Portfolio Allocation Pie ----------------
fig_alloc = go.Figure(
    go.Pie(
        labels=weights.index,
        values=weights.values,
        hole=0.4
    )
)
fig_alloc.update_layout(title="Portfolio Allocation")

# ---------------- Rolling Sharpe ----------------
rolling_sh = rolling_sharpe(port_ret, rf_rate, window)

fig_sharpe = go.Figure()
fig_sharpe.add_trace(go.Scatter(
    x=rolling_sh.index,
    y=rolling_sh.values,
    mode="lines",
    name="Rolling Sharpe"
))
fig_sharpe.update_layout(title="Rolling Portfolio Sharpe Ratio")

# ---------------- Regime Sharpe ----------------
regime_sh = regime_conditioned_sharpe(port_ret, rf_rate)

# ---------------- Bootstrap CI ----------------
ci_low, ci_high = bootstrap_ci(port_ret)

# ---------------- Distribution Fit ----------------
dist_results = fit_return_distribution(port_ret)

# ---------------- Layout ----------------
col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(fig_alloc, use_container_width=True)
    st.plotly_chart(fig_sharpe, use_container_width=True)

with col2:
    st.subheader("Summary Statistics")
    st.metric("Mean Daily Return", f"{port_ret.mean():.4%}")
    st.metric("Volatility", f"{port_ret.std():.4%}")
    st.metric("Sharpe (Full Sample)", f"{(port_ret.mean() / port_ret.std()) * (252**0.5):.2f}")

    st.write("**Bootstrap 95% CI (Mean Return)**")
    st.write(f"[{ci_low:.4%}, {ci_high:.4%}]")

    st.write("**Regime Sharpe Ratios**")
    st.dataframe(regime_sh)

    st.write("**Return Distribution Fit**")
    st.json(dist_results)

st.caption(
    "All metrics are probabilistic estimates. This dashboard is for research and educational use only."
)
