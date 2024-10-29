import streamlit as st
import yfinance as yf
import time
from datetime import datetime

class BankNiftyCPR:
    def __init__(self):
        self.top_cpr = None
        self.bottom_cpr = None
        self.check_count = 0
        self.max_checks = 10  # Set maximum number of checks

    def calculate_cpr(self):
        # Define Bank Nifty symbol and fetch previous day's data
        ticker_symbol = "^NSEBANK"
        bank_nifty = yf.Ticker(ticker_symbol)
        data = bank_nifty.history(period="5d")  # Fetch the last 5 days to ensure previous day's data
        
        if len(data) < 2:  # Ensure there's enough data
            return None, None
        
        previous_day = data.iloc[-2]  # Select the previous day's row

        # Extract High, Low, and Close values
        high = previous_day['High']
        low = previous_day['Low']
        close = previous_day['Close']

        # Calculate Top and Bottom CPR (TC and BC)
        pivot_point = (high + low + close) / 3
        self.top_cpr = (high + low) / 2
        self.bottom_cpr = (pivot_point - (high - low) / 2)

        return self.top_cpr, self.bottom_cpr

    def check_signals(self):
        # Fetch the latest price of Bank Nifty with a valid period
        ticker_symbol = "^NSEBANK"
        bank_nifty = yf.Ticker(ticker_symbol)
        latest_data = bank_nifty.history(period="1d", interval="1m")  # Use interval="1m" with period="1d"

        # Ensure latest_data is not empty
        if not latest_data.empty:
            current_price = latest_data['Close'].iloc[-1]  # Use iloc[-1] to get the last value safely
            return current_price
        else:
            return None

def main():
    st.title("Bank Nifty CPR Monitoring")
    cpr_monitor = BankNiftyCPR()

    if st.button("Calculate CPR"):
        top_cpr, bottom_cpr = cpr_monitor.calculate_cpr()
        
        if top_cpr is not None and bottom_cpr is not None:
            st.success(f"Top CPR (TC): {top_cpr}")
            st.success(f"Bottom CPR (BC): {bottom_cpr}")
            st.session_state.top_cpr = top_cpr
            st.session_state.bottom_cpr = bottom_cpr
        else:
            st.error("Not enough data to calculate CPR.")

    if 'top_cpr' in st.session_state and 'bottom_cpr' in st.session_state:
        current_price = cpr_monitor.check_signals()
        
        if current_price is not None:
            st.write(f"Current Price: {current_price}")

            # Check for buy and put signals
            if current_price == st.session_state.top_cpr:
                st.success(f"Buy Signal! Current Price: {current_price} has touched Top CPR: {st.session_state.top_cpr}")
            elif current_price == st.session_state.bottom_cpr:
                st.success(f"Put Signal! Current Price: {current_price} has touched Bottom CPR: {st.session_state.bottom_cpr}")
            else:
                st.warning(f"Current Price: {current_price} is not at CPR levels. No signal.")
        else:
            st.error("No data available for the latest price.")

    st.write("### Monitoring will update every 5 seconds.")
    while True:
        time.sleep(5)  # You can adjust this interval as needed
        if 'top_cpr' in st.session_state and 'bottom_cpr' in st.session_state:
            current_price = cpr_monitor.check_signals()
            if current_price is not None:
                st.write(f"Current Price: {current_price}")

                # Check for buy and put signals
                if current_price == st.session_state.top_cpr:
                    st.success(f"Buy Signal! Current Price: {current_price} has touched Top CPR: {st.session_state.top_cpr}")
                elif current_price == st.session_state.bottom_cpr:
                    st.success(f"Put Signal! Current Price: {current_price} has touched Bottom CPR: {st.session_state.bottom_cpr}")
                else:
                    st.warning(f"Current Price: {current_price} is not at CPR levels. No signal.")

if __name__ == "__main__":
    main()
