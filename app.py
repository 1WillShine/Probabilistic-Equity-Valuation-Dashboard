import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta
from src.bootstrap import rolling_bootstrap_ci
from src.visualization import animated_ci_band

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




# --------------------------------------------------
# Sidebar — Portfolio Builder
# --------------------------------------------------
with st.sidebar:
    st.header("Portfolio Builder")

    available_tickers = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "META",
        "NVDA", "TSLA", "JPM", "V", "SPY", "QQQ"
    ]

    selected = st.multiselect(
        "Select assets",
        available_tickers,
        default=["AAPL", "MSFT"]
    )

    st.subheader("Holdings (Quantities)")
    quantities = {}
    for t in selected:
        quantities[t] = st.number_input(
            f"{t} shares",
            min_value=0.0,
            value=10.0,
            step=1.0
        )

    start_date = st.date_input(
        "Start date",
        date.today() - timedelta(days=365 * 3)
    )
    end_date = st.date_input("End date", date.today())

    rf_rate = st.number_input(
        "Risk-free rate (annual)",
        value=0.03,
        step=0.005
    )

    window = st.slider(
        "Rolling Sharpe window (days)",
        30, 252, 126
    )

# --------------------------------------------------
# Validate portfolio
# --------------------------------------------------
if not selected:
    st.warning("Select at least one asset.")
    st.stop()

qty_series = pd.Series(quantities)
qty_series = qty_series[qty_series > 0]

if qty_series.empty:
    st.warning("Enter at least one positive quantity.")
    st.stop()

weights = qty_series / qty_series.sum()

# --------------------------------------------------
# Fetch prices (robust)
# --------------------------------------------------
@st.cache_data(ttl=3600)
def load_prices(tickers, start, end):
    dfs = []
    valid = []

    for t in tickers:
        df = fetch_stock(t, start, end)
        if df is not None:
            dfs.append(df)
            valid.append(t)
        else:
            st.warning(f"⚠️ Data unavailable for {t}, skipped.")

    if not dfs:
        return None, None

    prices = pd.concat(dfs, axis=1).dropna()
    return prices, valid

prices, valid_tickers = load_prices(weights.index.tolist(), start_date, end_date)

if prices is None:
    st.error("No valid price data available.")
    st.stop()

weights = weights.loc[valid_tickers]

# --------------------------------------------------
# Analytics
# --------------------------------------------------
returns = compute_returns(prices)
port_ret = portfolio_returns(returns, weights)

rolling_sh = rolling_sharpe(port_ret, rf_rate, window)
regime_sh = regime_conditioned_sharpe(port_ret, rf_rate)
ci_low, ci_high = bootstrap_ci(port_ret)
dist_stats = fit_return_distribution(port_ret)

# --------------------------------------------------
# Visualizations
# --------------------------------------------------
alloc_fig = go.Figure(
    go.Pie(
        labels=weights.index,
        values=weights.values,
        hole=0.45
    )
)
alloc_fig.update_layout(title="Portfolio Allocation")

sharpe_fig = go.Figure()
sharpe_fig.add_trace(go.Scatter(
    x=rolling_sh.index,
    y=rolling_sh.values,
    mode="lines",
    name="Rolling Sharpe"
))
sharpe_fig.update_layout(title="Rolling Portfolio Sharpe")
# --------------------------------------------------
# Rolling Bootstrap CI (NOW port_ret EXISTS)
# --------------------------------------------------
ci_df = rolling_bootstrap_ci(
    port_ret,
    window=window,
    n_boot=800
)

st.subheader("🎞 Rolling Return Uncertainty")

ci_fig = animated_ci_band(ci_df)
st.plotly_chart(ci_fig, use_container_width=True)

st.info(
    "The shaded region shows the 95% bootstrap confidence interval "
    "for the rolling mean return. Narrow bands indicate stability; "
    "widening bands indicate increased uncertainty."
)

# --------------------------------------------------
# Layout
# --------------------------------------------------
col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(alloc_fig, use_container_width=True)
    st.plotly_chart(sharpe_fig, use_container_width=True)

with col2:
    st.subheader("Portfolio Summary")

    st.metric(
        "Mean Daily Return",
        f"{port_ret.mean():.3%}"
    )
    st.metric(
        "Annualized Volatility",
        f"{port_ret.std() * (252 ** 0.5):.2%}"
    )
    st.metric(
        "Sharpe Ratio",
        f"{(port_ret.mean() / port_ret.std()) * (252 ** 0.5):.2f}"
    )

    st.write("**95% Bootstrap CI (Mean Return)**")
    st.write(f"[{ci_low:.3%}, {ci_high:.3%}]")

    st.write("**Regime-Conditioned Sharpe**")
    st.dataframe(regime_sh)

    st.write("**Return Distribution Diagnostics**")
    st.json(dist_stats)

st.caption(
    "Probabilistic estimates only. Not investment advice."
)
