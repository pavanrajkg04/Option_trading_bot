import yfinance as yf
import time
from datetime import datetime

# Set a limit for testing purposes
check_count = 0
max_checks = 10  # Set maximum number of checks

def calculate_cpr():
    global top_cpr, bottom_cpr  # Use global variables to store top and bottom CPR for access in other functions

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

    # Print calculated CPR levels
    print(f"[{datetime.now()}] CPR Calculated")
    print(f"Top CPR (TC): {top_cpr}")
    print(f"Bottom CPR (BC): {bottom_cpr}")
    print("Monitoring for Buy and Put Signals...")

# Function to check for buy and put signals
def check_signals():
    global top_cpr, bottom_cpr, check_count

    # Fetch the latest price of Bank Nifty with a valid period
    ticker_symbol = "^NSEBANK"
    bank_nifty = yf.Ticker(ticker_symbol)
    latest_data = bank_nifty.history(period="1d", interval="1m")  # Use interval="1m" with period="1d"

    # Ensure latest_data is not empty
    if not latest_data.empty:
        current_price = latest_data['Close'].iloc[-1]  # Use iloc[-1] to get the last value safely

        # Check for buy signal (current price crosses above top CPR)
        if current_price >= top_cpr:
            print(f"[{datetime.now()}] Buy Signal! Current Price: {current_price} has touched and is above Top CPR: {top_cpr}")

        # Check for put signal (current price crosses below bottom CPR)
        elif current_price <= bottom_cpr:
            print(f"[{datetime.now()}] Put Signal! Current Price: {current_price} has touched and is below Bottom CPR: {bottom_cpr}")
        
        else:
            print(f"[{datetime.now()}] Current Price: {current_price} is between CPR levels. No signal.")

        check_count += 1  # Increment the check count
    else:
        print(f"[{datetime.now()}] No data available for the latest price.")

# Calculate CPR immediately for testing
calculate_cpr()

# Monitoring loop with a limit on checks for testing purposes
while True:
    if 'top_cpr' in globals() and 'bottom_cpr' in globals():  # Check if CPR levels have been calculated
        check_signals()
    time.sleep(5)  # Adjust this interval as needed

print("Script completed after reaching max checks.")
