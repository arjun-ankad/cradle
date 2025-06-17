import os
import requests
import pandas as pd
from datetime import datetime, timedelta

# CONFIGURATION
API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://api.marketdata.app/v1/options/history"
OUTPUT_FOLDER = "cache/options/"
TICKER_FILE = "cache/tickers.csv"

# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load tickers
tickers = pd.read_csv(TICKER_FILE)["Ticker"].dropna().unique()

# Set date range for 3 years
end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=3*365)).strftime('%Y-%m-%d')

# Fetch data
for ticker in tickers:
    print(f"Fetching historical options for {ticker} from {start_date} to {end_date}...")
    try:
        params = {
            "symbol": ticker,
            "start": start_date,
            "end": end_date,
            "api_key": Vms2VzVRNF8xeWVycktLSW40cXFHSEtRR3pUZ25aRTdNS0tTbGRhdUs3OD0,
        }

        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise error for bad response

        data = response.json()
        if "data" in data and data["data"]:
            df = pd.DataFrame(data["data"])
            out_path = os.path.join(OUTPUT_FOLDER, f"{ticker}_options.csv")
            df.to_csv(out_path, index=False)
            print(f"Saved data to {out_path}")
        else:
            print(f"No data found for {ticker}")

    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
