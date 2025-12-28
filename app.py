import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import date, timedelta

from src.data_fetch import fetch_stock, fetch_wilshire_and_gdp, fetch_buffett_fallback
from src.analysis import compute_log_trend, compute_smooth_trend, pct_distance
from src.bootstrap import bootstrap_sharpe

st.set_page_config(layout="wide", page_title="Probabilistic Equity Valuation")

st.title("📈 Probabilistic Equity Valuation & Metric Stability Dashboard")

st.markdown(
"""
This dashboard evaluates **equity valuation metrics under uncertainty**.
Rather than presenting point estimates, it visualizes **confidence intervals,
distributional assumptions, and metric stability**.
"""
)

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Inputs")
    ticker = st.text_input("Ticker", value="AAPL").upper()
    end_date = st.date_input("End date", date.today())
    start_date = st.date_input("Start date", end_date - timedelta(days=365*3))
    trend_type = st.selectbox("Trend model", ["CAGR (log-linear)", "Smoothed log trend"])
    smooth_window = st.slider("Smoothing window", 5, 251, 63)

# ---------------- Data ----------------
@st.cache_data(ttl=3600)
def get_data(ticker, start, end):
    stock = fetch_stock(ticker, start, end)
    try:
        buffett = fetch_wilshire_and_gdp(start, end)
    except Exception:
        buffett = fetch_buffett_fallback(start, end)
    return stock, buffett

stock_df, buffett_df = get_data(ticker, start_date, end_date)

if stock_df.empty:
    st.error("No data available.")
    st.stop()

price = stock_df.iloc[:, 0].rename("price")

# ---------------- Trend ----------------
if trend_type == "CAGR (log-linear)":
    trend = compute_log_trend(price)
else:
    trend = compute_smooth_trend(price, window=smooth_window)

dist_pct = pct_distance(price.loc[trend.index], trend).iloc[-1]

# ---------------- Returns ----------------
returns = price.pct_change().dropna()

# ---------------- Bootstrap Sharpe ----------------
sharpe_ci = bootstrap_sharpe(returns)

# ---------------- Price Plot ----------------
fig_price = go.Figure()
fig_price.add_trace(go.Scatter(x=price.index, y=price, name="Price"))
fig_price.add_trace(go.Scatter(x=trend.index, y=trend, name="Ideal trend", line=dict(dash="dash")))
fig_price.update_layout(
    title=f"{ticker}: Price vs Statistical Trend",
    height=450
)

# ---------------- Return Distribution ----------------
fig_ret = go.Figure()
fig_ret.add_trace(go.Histogram(x=returns, nbinsx=50))
fig_ret.update_layout(
    title="Return Distribution",
    height=300
)

# ---------------- Buffett ----------------
fig_buffett = None
if buffett_df is not None and not buffett_df.empty:
    fig_buffett = go.Figure()
    fig_buffett.add_trace(go.Scatter(
        x=buffett_df.index,
        y=buffett_df["buffett_ratio"] * 100,
        name="Buffett Indicator (%)"
    ))
    fig_buffett.update_layout(
        title="Buffett Indicator (Market Cap / GDP)",
        height=300
    )

# ---------------- Layout ----------------
col1, col2 = st.columns([3, 1])

with col1:
    st.plotly_chart(fig_price, use_container_width=True)
    st.plotly_chart(fig_ret, use_container_width=True)
    if fig_buffett:
        st.plotly_chart(fig_buffett, use_container_width=True)

with col2:
    st.subheader("Summary")
    st.metric("Distance from trend", f"{dist_pct:.2f}%")
    st.metric("Sharpe (mean)", f"{sharpe_ci['mean']:.2f}")
    st.metric("Sharpe 90% CI", f"[{sharpe_ci['lower']:.2f}, {sharpe_ci['upper']:.2f}]")

    if sharpe_ci["lower"] < 0:
        st.warning("Sharpe confidence interval includes zero → unstable risk-adjusted returns.")
    else:
        st.success("Sharpe ratio statistically positive.")

st.caption(
"All outputs are statistical estimates, not investment advice. "
"Models assume stationarity and historical representativeness."
)

