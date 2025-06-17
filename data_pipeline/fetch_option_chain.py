import os
import pandas as pd
import yfinance as yf

# Paths
tickers_csv_path = 'cache/tickers.csv'
options_folder = 'cache/options/'

# Create output folder if it doesn't exist
os.makedirs(options_folder, exist_ok=True)

# Load tickers
df = pd.read_csv(tickers_csv_path)
tickers = df["Ticker"].dropna().unique()

for ticker in tickers:
    try:
        print(f"Fetching options for {ticker}")
        tkr = yf.Ticker(ticker)
        all_data = []

        for exp in tkr.options:
            opt = tkr.option_chain(exp)
            calls = opt.calls.copy()
            calls["type"] = "call"
            calls["expirationDate"] = exp

            puts = opt.puts.copy()
            puts["type"] = "put"
            puts["expirationDate"] = exp

            all_data.append(calls)
            all_data.append(puts)

        if all_data:
            options_df = pd.concat(all_data, ignore_index=True)
            out_path = os.path.join(options_folder, f"{ticker}_options.csv")
            options_df.to_csv(out_path, index=False)
            print(f"Saved: {out_path}")
        else:
            print(f"No data found for {ticker}")
    
    except Exception as e:
        print(f"Error for {ticker}: {e}")
