Probabilistic Equity Valuation & Metric Stability Dashboard
-----------------------------------------------------------

A quantitative finance dashboard that evaluates **how reliable common equity metrics actually are**, using probability theory, resampling, and statistical modeling.

### Motivation

Most retail and professional platforms report **point estimates**:

*   Sharpe ratio
    
*   Expected return
    
*   Fair value trend
    

This project instead asks:

> _How stable are these metrics under resampling and uncertainty?_

### Core Features

#### 1\. Statistical Price Trends

*   Log-linear (CAGR) growth model
    
*   Smoothed log-space trend
    
*   Percent deviation from ideal trajectory
    

#### 2\. Metric Stability via Bootstrapping

*   Bootstrap resampling of returns
    
*   Confidence intervals for Sharpe ratio
    
*   Visualization of estimation uncertainty
    

#### 3\. Distributional Return Analysis

*   Empirical return distribution
    
*   Sensitivity to volatility clustering
    
*   Sample-size awareness
    

#### 4\. Macro Valuation Context

*   Buffett Indicator (Market Cap / GDP)
    
*   FRED-backed with automatic fallback
    

### Methodology

**Trend Modeling**

*   Prices modeled in log space
    
*   Trends represent statistical baselines, not targets
    

**Bootstrap Inference**

*   Returns resampled with replacement
    
*   Sharpe ratio distribution estimated empirically
    
*   Confidence intervals reflect estimation uncertainty
    

**Interpretation**

*   Wide confidence intervals → unstable metric
    
*   CI crossing zero → weak risk-adjusted evidence
    

### Assumptions

*   Returns are weakly stationary within sample window
    
*   Historical returns approximate future variability
    
*   Sharpe ratio meaningful only under finite variance
    
*   No transaction costs or slippage modeled
    

### Limitations

*   Regime shifts invalidate stationarity assumptions
    
*   Bootstrap does not correct structural bias
    
*   Macro valuation signals are descriptive, not predictive
    
*   Trend deviations are statistical, not fundamental
    

### Tech Stack

*   **Python**: pandas, NumPy
    
*   **Visualization**: Plotly
    
*   **Dashboard**: Streamlit
    
*   **Data**: Yahoo Finance, FRED API
    

## Methodology in Details

### Ideal Trend Models

1. Log-linear (CAGR) model  
   - Apply log transform to prices  
   - Fit linear regression over time  
   - Exponentiate fitted line back to price space  
   - Represents long-term exponential growth

2. Smoothed log trend  
   - Log-transform the price  
   - Apply polynomial smoothing  
   - Noise-reduced fair-value curve  

### Deviation Metric

Deviation (%) = (Actual Price - Ideal Price) / Ideal Price * 100

Interpretation:  
Above 20%: likely overvalued  
0% to 20%: slightly overvalued  
0% to -20%: slightly undervalued  
Below -20%: undervalued

### Buffett Indicator

Buffett Ratio = Total Market Cap / GDP

Interpretation:  
Below 70%: undervalued  
Around 100%: fairly valued  
Above 120%: overvalued  
Above 150%: highly overvalued

## License

MIT License

## Acknowledgements

- Yahoo Finance  
- FRED (Federal Reserve Economic Data)  
- Streamlit and Plotly documentation


### Disclaimer

This project is for **educational and research purposes only**and does not constitute investment advice.


## Running the Project

1. Install dependencies:  pip install -r requirements.txt
2. Run the Streamlit app: streamlit run app/main.py



