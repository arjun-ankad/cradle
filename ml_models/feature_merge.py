import os
import pandas as pd
import numpy as np

# Get directory paths relative to this script
base_dir = os.path.dirname(os.path.abspath(__file__))
sentiment_dir = os.path.join(base_dir, "../data_pipeline/cache/sentiment")
volatility_dir = os.path.join(base_dir, "../data_pipeline/cache/volatility")
price_regime_dir = os.path.join(base_dir, "../data_pipeline/cache/preprocessed")
output_path = os.path.join(base_dir, "../data_pipeline/cache/features.csv")

# Initialize merged dataframe list
merged_rows = []

# Loop through tickers (based on sentiment files)
for fname in os.listdir(sentiment_dir):
    if not fname.endswith("_sentiment_score.csv"):
        continue
    ticker = fname.replace("_sentiment_score.csv", "")

    try:
        sentiment_path  = os.path.join(sentiment_dir, fname)
        volatility_path = os.path.join(volatility_dir, f"{ticker}_OHLCV_volatility.csv")
        labels_path     = os.path.join(price_regime_dir, f"{ticker}_OHLCV_labels.csv")

        df_sent = pd.read_csv(sentiment_path)
        df_vol  = pd.read_csv(volatility_path)
        df_lab  = pd.read_csv(labels_path)

        # --- make dtypes identical ---------------------------------
        df_sent["timestamp"] = pd.to_datetime(df_sent["timestamp"]).dt.tz_localize(None)
        df_vol["datetime"]   = pd.to_datetime(df_vol["datetime"])  # already naïve
        # -----------------------------------------------------------

        # nearest-prior merge (≤1 day tolerance)
        merged = pd.merge_asof(
            df_vol.sort_values("datetime"),
            df_sent.sort_values("timestamp"),
            left_on="datetime",
            right_on="timestamp",
            direction="backward",
            tolerance=pd.Timedelta("1D")
        )

        if merged.empty:
            print(f"No time overlap for {ticker}, skipping.")
            continue

        # add regime labels, truncate to whichever side is shorter
        n = min(len(merged), len(df_lab))
        merged = merged.iloc[:n]
        merged["price_regime"] = df_lab["label"].iloc[:n].values
        merged["ticker"] = ticker

        merged = merged[["datetime", "ticker", "score", "volatility", "price_regime"]]
        merged.columns = ["timestamp", "ticker",
                          "sentiment_score", "volatility", "price_regime"]

        merged_rows.append(merged)
        print(f"Merged features for {ticker}")

    except FileNotFoundError as fe:
        print(f"Missing file for {ticker}: {fe}")
    except Exception as e:
        print(f"Error merging {ticker}: {e}")
# Combine all tickers
final_df = pd.concat(merged_rows, ignore_index=True)
final_df.to_csv(output_path, index=False)
print(f"Final merged features saved to: {output_path}")
