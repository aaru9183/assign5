import pandas as pd
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="MSFT Sharpe Ratio", page_icon="📈")
st.title("Microsoft (MSFT) Monthly Sharpe Ratio")
st.caption("AC420 Assignment #5 | Aarav Zaveri")

@st.cache_data(ttl=3600)
def load_prices():
    return yf.download(
        "MSFT", period="5y", interval="1mo", auto_adjust=True,
        multi_level_index=False, progress=False,
    )

try:
    data = load_prices()
except Exception:
    st.error("Unable to download MSFT data. Please try again shortly.")
    st.stop()

if data is None or data.empty:
    st.error("No MSFT data found. Please try again shortly.")
    st.stop()

close_prices = data["Close"].dropna()
monthly_returns = close_prices.pct_change(fill_method=None).dropna()
rf_monthly = 0.0025
std_dev_return = monthly_returns.std()

if len(monthly_returns) < 2 or pd.isna(std_dev_return) or std_dev_return == 0:
    st.error("Insufficient return variation to calculate the Sharpe ratio.")
    st.stop()

mean_excess_return = (monthly_returns - rf_monthly).mean()
monthly_sharpe_ratio = mean_excess_return / std_dev_return
st.metric(label="Monthly Sharpe Ratio", value=f"{monthly_sharpe_ratio:.3f}")
st.write("Based on five years of monthly MSFT closing prices from Yahoo Finance via yfinance.")
st.caption("Monthly risk-free rate: 0.25%. Sharpe ratio = average monthly excess return / sample standard deviation of monthly returns. Prices are adjusted for dividends and splits. The latest monthly observation may be a partial month.")
