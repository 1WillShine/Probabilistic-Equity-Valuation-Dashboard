📈 Probabilistic Equity Valuation & Metric Stability Dashboard
==============================================================

_Quantifying Estimation Risk in Financial Metrics_

Motivation
----------

Most financial platforms report performance metrics such as Sharpe ratio, expected return, or valuation trends as single point estimates. As a student learning probability theory and quantitative finance, I became interested in how reliable these metrics actually are given limited data, market noise, and regime changes. This project applies probabilistic inference to quantify the uncertainty behind commonly used financial metrics rather than treating them as deterministic truths.

Project Overview
----------------

This dashboard evaluates the statistical stability of equity and portfolio metrics using resampling, distribution diagnostics, and probabilistic visualization. Instead of asking whether a metric is “good” or “bad,” the system asks how uncertain that metric is and whether it is statistically meaningful. The result is a framework that highlights estimation risk and discourages overconfidence in point estimates.

Methodology
-----------

Prices are modeled in log space to reflect their multiplicative growth structure, allowing long-term trends to be interpreted as statistical baselines rather than targets. Returns are analyzed using bootstrap resampling to empirically estimate the sampling distributions of metrics such as mean return and Sharpe ratio without imposing normality assumptions. Confidence intervals are computed using percentile-based methods, and return distributions are evaluated for skewness, kurtosis, and fat tails using both normal and Student-t fits.

Interpretation Framework
------------------------

Wide confidence intervals indicate unstable or weakly supported metrics, while intervals crossing zero suggest little statistical evidence of risk-adjusted performance. Rolling bootstrap windows are used to detect regime-dependent instability over time. Macro valuation context is provided through the Buffett Indicator, which is presented descriptively rather than predictively.

Results & Insights
------------------

The analysis shows that many commonly cited performance metrics are far less stable than their point estimates suggest, especially over short samples or volatile regimes. Heavy tails and skewness dominate empirical return distributions, reinforcing the limitations of Gaussian assumptions. The project demonstrates that estimation risk is often as important as expected return when interpreting financial performance.

Technical Stack
---------------

The project is built in Python using pandas and NumPy for computation, SciPy for statistical diagnostics, Plotly for interactive visualization, and Streamlit for dashboard deployment. Financial data is sourced from Yahoo Finance, with macroeconomic data from FRED and fallback logic to handle missing data and rate limits.

Assumptions & Limitations
-------------------------

Returns are assumed to be weakly stationary within rolling windows, and transaction costs are not modeled. Bootstrap inference captures sampling uncertainty but does not correct for structural bias or regime shifts. Valuation signals are descriptive and not intended as investment recommendations.

How to Run
----------

Install dependencies using pip install -r requirements.txt, then run the application with streamlit run app/main.py.

Disclaimer
----------

This project is for educational and research purposes only and does not constitute investment advice.
