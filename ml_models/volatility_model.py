import os
import pandas as pd
import numpy as np

# Parameters
window = 21  # Rolling window size
trading_days = 252  # Annualization factor

# Define directories
ohlcv_dir = os.path.join(os.path.dirname(__file__), "../data_pipeline/cache/ohlcv")
output_dir = os.path.join(os.path.dirname(__file__), "../data_pipeline/cache/volatility")
os.makedirs(output_dir, exist_ok=True)

def compute_volatility(df):
    # Sort and compute log returns
    df = df.sort_values("datetime")
    df["log_return"] = np.log(df["close"] / df["close"].shift(1))

    # Rolling volatility (standard deviation of log returns)
    df["volatility"] = df["log_return"].rolling(window=window).std()

    # Annualize volatility
    df["volatility"] *= np.sqrt(trading_days)

    return df[["datetime", "volatility"]].dropna()

# Loop through each ticker's OHLCV file
for filename in os.listdir(ohlcv_dir):
    if not filename.endswith(".csv"):
        continue

    ticker = filename.replace(".csv", "")
    filepath = os.path.join(ohlcv_dir, filename)

    try:
        df = pd.read_csv(filepath, sep=';', parse_dates=['datetime'])
        result_df = compute_volatility(df)
        result_df.to_csv(os.path.join(output_dir, f"{ticker}_volatility.csv"), index=False)
        print(f"Saved: {ticker}_volatility.csv")
    except Exception as e:
        print(f"Error processing {ticker}: {e}")

