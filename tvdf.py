# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 22:47:43 2025

@author: Hemal
"""

import streamlit as st
from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import matplotlib.pyplot as plt

# Initialize the TvDatafeed client
data_client = TvDatafeed()

# Streamlit app title
st.title("Stock Data Visualization")

# User inputs
symbol = st.text_input("Enter the symbol (e.g., NIFTY250327C23400):")
exchange = st.text_input("Enter the exchange (e.g., NSE):")
interval = st.selectbox("Select the interval:", [Interval.in_daily, Interval.in_weekly, Interval.in_monthly])

# Fetch data button
if st.button("Fetch Data"):
    if symbol and exchange and interval:
        # Fetch the historical data
        data = data_client.get_hist(symbol, exchange, interval)

        # Ensure data is a DataFrame
        if isinstance(data, pd.DataFrame):
            # Display the data
            st.write("Fetched Data:")
            st.write(data)

            # Plot the data
            st.write("Data Visualization:")
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})

            # Plot price data
            ax1.plot(data.index, data['open'], label='Open Price', color='blue')
            ax1.plot(data.index, data['high'], label='High Price', color='green')
            ax1.plot(data.index, data['low'], label='Low Price', color='red')
            ax1.plot(data.index, data['close'], label='Close Price', color='purple')
            ax1.set_title(f'{symbol} Price Data')
            ax1.set_ylabel('Price')
            ax1.legend()

            # Plot volume data
            ax2.bar(data.index, data['volume'], color='gray', alpha=0.3, label='Volume')
            ax2.set_ylabel('Volume')
            ax2.legend(loc='upper left')

            # Show plot
            st.pyplot(fig)
        else:
            st.error("Data fetched is not in the expected format.")
    else:
        st.warning("Please enter all the required fields.")
