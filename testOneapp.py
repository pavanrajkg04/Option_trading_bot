import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate CPR levels
def calculate_cpr(df):
    df['Pivot'] = (df['High'] + df['Low'] + df['Close']) / 3
    df['BC'] = (df['High'] + df['Low']) / 2
    df['TC'] = df['Pivot'] + (df['Pivot'] - df['BC'])
    return df

# Function to implement the CPR strategy
def apply_cpr_strategy(df, target=30, stop_loss=10):
    df['Signal'] = 0
    df['Entry_Price'] = np.nan
    df['Exit_Price'] = np.nan
    df['Trade'] = np.nan
    
    for i in range(1, len(df)):
        # Buy condition: Today's Pivot > Previous Pivot and Close crosses above TC
        if df['Pivot'][i] > df['Pivot'][i-1] and df['Close'][i] > df['TC'][i]:
            df.loc[i, 'Signal'] = 1
            df.loc[i, 'Entry_Price'] = df['Close'][i]
            df.loc[i, 'Exit_Price'] = df['Entry_Price'][i] + target
            df.loc[i, 'Trade'] = 'Buy'

        # Sell condition: Today's Pivot < Previous Pivot and Close crosses below BC
        elif df['Pivot'][i] < df['Pivot'][i-1] and df['Close'][i] < df['BC'][i]:
            df.loc[i, 'Signal'] = -1
            df.loc[i, 'Entry_Price'] = df['Close'][i]
            df.loc[i, 'Exit_Price'] = df['Entry_Price'][i] - target
            df.loc[i, 'Trade'] = 'Sell'
    
    # Calculate profit or loss for each trade
    df['PnL'] = np.where(
        df['Signal'] == 1,  # Buy signal
        np.where(df['Close'] >= df['Exit_Price'], target, np.where(df['Close'] <= df['Entry_Price'] - stop_loss, -stop_loss, 0)),
        np.where(df['Signal'] == -1,  # Sell signal
                 np.where(df['Close'] <= df['Exit_Price'], target, np.where(df['Close'] >= df['Entry_Price'] + stop_loss, -stop_loss, 0)),
                 0)
    )
    
    df['Cumulative_PnL'] = df['PnL'].cumsum()
    return df

# Streamlit app layout
st.title("CPR-Based Trading Strategy with Target and Stop Loss")
st.write("This app backtests a CPR-based trading strategy on historical stock data.")

# User inputs
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL):", value="AAPL")
start_date = st.date_input("Start Date", pd.to_datetime("2022-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("2023-01-01"))
target = st.number_input("Target Points", value=30)
stop_loss = st.number_input("Stop Loss Points", value=10)

if st.button("Run Backtest"):
    # Load data
    data = yf.download(ticker, start=start_date, end=end_date)
    data = data[['High', 'Low', 'Close']]
    
    # Calculate CPR and apply the strategy
    data = calculate_cpr(data)
    data = apply_cpr_strategy(data, target, stop_loss)
    
    # Display results
    st.write("Backtest Results:")
    st.write(data[['High', 'Low', 'Close', 'Pivot', 'BC', 'TC', 'Signal', 'PnL', 'Cumulative_PnL']])
    
    # Plot the CPR levels and trade signals
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.plot(data['Close'], label="Close Price", color='black')
    ax.plot(data['Pivot'], label="Pivot", color='blue', linestyle='--')
    ax.plot(data['BC'], label="Bottom CPR", color='red', linestyle='--')
    ax.plot(data['TC'], label="Top CPR", color='green', linestyle='--')
    
    # Plot buy and sell signals
    buy_signals = data[data['Trade'] == 'Buy']
    sell_signals = data[data['Trade'] == 'Sell']
    ax.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='green', label='Buy Signal', s=100)
    ax.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='red', label='Sell Signal', s=100)
    
    ax.set_title(f"CPR-Based Strategy Backtest for {ticker}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    
    st.pyplot(fig)
    
    # Plot cumulative PnL
    st.write("Cumulative Profit and Loss:")
    st.line_chart(data['Cumulative_PnL'])
