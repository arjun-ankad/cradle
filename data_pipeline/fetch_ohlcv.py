
# import os
# import requests

# # Replace with your actual API key
# API_KEY = "9dbf43d2861a4e309d9b7ae750fdb318"
# TICKER = "NVDA"
# INTERVAL = "30min"
# OUTPUTSIZE = "5000"
# FILENAME = f"{TICKER}_OHLCV.csv"

# # Ensure the output directory exists
# output_dir = "cache/ohlcv"
# os.makedirs(output_dir, exist_ok=True)
# output_path = os.path.join(output_dir, FILENAME)

# # Construct the Twelve Data API URL
# url = (
#     f"https://api.twelvedata.com/time_series"
#     f"?symbol={TICKER}"
#     f"&interval={INTERVAL}"
#     f"&outputsize={OUTPUTSIZE}"
#     f"&format=CSV"
#     f"&filename={FILENAME}"
#     f"&apikey={API_KEY}"
# )

# # Download and save the CSV file
# try:
#     response = requests.get(url)
#     response.raise_for_status()
#     with open(output_path, "wb") as f:
#         f.write(response.content)
#     print(f"Saved OHLCV data for {TICKER} to {output_path}")
# except Exception as e:
#     print(f"Error fetching data for {TICKER}: {e}")

import os
import time
import requests
import pandas as pd

# Your Twelve Data API key
API_KEY = "9dbf43d2861a4e309d9b7ae750fdb318" 
OUTPUTSIZE = "5000"

# Load tickers from CSV
tickers_csv_path = "cache/tickers.csv"
tickers_df = pd.read_csv(tickers_csv_path)
tickers = tickers_df["Ticker"].head(10).tolist()

# Output directory
output_dir = "cache/ohlcv"
os.makedirs(output_dir, exist_ok=True)

# Fetch and save data for each ticker, one per minute
for i, ticker in enumerate(tickers):
    filename = f"{ticker}_OHLCV.csv"
    output_path = os.path.join(output_dir, filename)

    url = (
        f"https://api.twelvedata.com/time_series"
        f"?symbol={ticker}"
        f"&interval={INTERVAL}"
        f"&outputsize={OUTPUTSIZE}"
        f"&format=CSV"
        f"&filename={filename}"
        f"&apikey={API_KEY}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"[{i+1}/{len(tickers)}] Saved OHLCV data for {ticker} to {output_path}")
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")

    if i < len(tickers) - 1:
        print("Waiting 60 seconds before next call...")
        time.sleep(60)  # Respect Twelve Data's 1-call-per-minute limit
