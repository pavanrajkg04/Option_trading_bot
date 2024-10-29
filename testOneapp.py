import yfinance as yf
import streamlit as st
from datetime import datetime
import time

# Set up the Streamlit page
st.set_page_config(page_title="Bank Nifty CPR Signal", layout="centered")
st.title("Bank Nifty CPR Signal Monitoring")

# Global variables to store CPR levels
top_cpr = None
bottom_cpr = None

# Function to calculate CPR
def calculate_cpr():
    global top_cpr, bottom_cpr

    # Define Bank Nifty symbol and fetch previous day's data
    ticker_symbol = "^NSEBANK"
    bank_nifty = yf.Ticker(ticker_symbol)
    data = bank_nifty.history(period="5d")  # Fetch the last 5 days to ensure previous day's data
    previous_day = data.iloc[-2]  # Select the previous day's row

    # Extract High, Low, and Close values
    high = previous_day['High']
    low = previous_day['Low']
    close = previous_day['Close']

    # Calculate Top and Bottom CPR (TC and BC)
    pivot_point = (high + low + close) / 3
    top_cpr = (high + low) / 2
    bottom_cpr = (pivot_point - (high - low) / 2)

    # Display calculated CPR levels
    st.write(f"**[{datetime.now()}] CPR Calculated**")
    st.write(f"**Top CPR (TC):** {top_cpr}")
    st.write(f"**Bottom CPR (BC):** {bottom_cpr}")

# Function to check for buy and put signals
def check_signals():
    # Fetch the latest price of Bank Nifty with a valid period
    ticker_symbol = "^NSEBANK"
    bank_nifty = yf.Ticker(ticker_symbol)
    latest_data = bank_nifty.history(period="1d", interval="1m")  # Use interval="1m" with period="1d"

    # Ensure latest_data is not empty
    if not latest_data.empty:
        current_price = latest_data['Close'].iloc[-1]  # Use iloc[-1] to get the last value safely

        # Check for buy signal (current price crosses above top CPR)
        if current_price >= top_cpr:
            st.success(f"[{datetime.now()}] **Buy Signal!** Current Price: {current_price} has touched and is above Top CPR: {top_cpr}")

        # Check for put signal (current price crosses below bottom CPR)
        elif current_price <= bottom_cpr:
            st.error(f"[{datetime.now()}] **Put Signal!** Current Price: {current_price} has touched and is below Bottom CPR: {bottom_cpr}")

        else:
            st.write(f"[{datetime.now()}] Current Price: {current_price} is between CPR levels. No signal.")
    else:
        st.warning(f"[{datetime.now()}] No data available for the latest price.")

# Calculate CPR on the first run
if st.button("Calculate CPR"):
    calculate_cpr()

# Check signals every few seconds (Auto-refresh)
if top_cpr is not None and bottom_cpr is not None:
    st.write("Monitoring for Buy and Put Signals...")
    check_signals()

# Auto-refresh every 60 seconds
st_autorefresh = st.experimental_rerun
st_autorefresh(interval=60000, limit=100, key="signal_refresh")
