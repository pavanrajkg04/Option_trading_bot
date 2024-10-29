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
            print(f"[{datetime.now()}] Not enough data to calculate CPR.")
            return
        
        previous_day = data.iloc[-2]  # Select the previous day's row

        # Extract High, Low, and Close values
        high = previous_day['High']
        low = previous_day['Low']
        close = previous_day['Close']

        # Calculate Top and Bottom CPR (TC and BC)
        pivot_point = (high + low + close) / 3
        self.top_cpr = (high + low) / 2
        self.bottom_cpr = (pivot_point - (high - low) / 2)

        # Print calculated CPR levels
        print(f"[{datetime.now()}] CPR Calculated")
        print(f"Top CPR (TC): {self.top_cpr}")
        print(f"Bottom CPR (BC): {self.bottom_cpr}")
        print("Monitoring for Buy and Put Signals...")

    def check_signals(self):
        # Fetch the latest price of Bank Nifty with a valid period
        ticker_symbol = "^NSEBANK"
        bank_nifty = yf.Ticker(ticker_symbol)
        latest_data = bank_nifty.history(period="1d", interval="1m")  # Use interval="1m" with period="1d"

        # Ensure latest_data is not empty
        if not latest_data.empty:
            current_price = latest_data['Close'].iloc[-1]  # Use iloc[-1] to get the last value safely

            # Check for buy signal (current price touches top CPR)
            if current_price == self.top_cpr:
                print(f"[{datetime.now()}] Buy Signal! Current Price: {current_price} has touched Top CPR: {self.top_cpr}")

            # Check for put signal (current price touches bottom CPR)
            elif current_price == self.bottom_cpr:
                print(f"[{datetime.now()}] Put Signal! Current Price: {current_price} has touched Bottom CPR: {self.bottom_cpr}")
            
            else:
                print(f"[{datetime.now()}] Current Price: {current_price} is not at CPR levels. No signal.")

            self.check_count += 1  # Increment the check count
        else:
            print(f"[{datetime.now()}] No data available for the latest price.")

    def run_monitoring(self):
        # Calculate CPR immediately
        self.calculate_cpr()

        # Monitoring loop with a limit on checks for testing purposes
        while self.check_count < self.max_checks:
            if self.top_cpr is not None and self.bottom_cpr is not None:  # Check if CPR levels have been calculated
                self.check_signals()
            time.sleep(5)  # Adjust this interval as needed

        print("Script completed after reaching max checks.")

# Create an instance of the BankNiftyCPR class and start monitoring
cpr_monitor = BankNiftyCPR()
cpr_monitor.run_monitoring()
