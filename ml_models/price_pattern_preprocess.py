import os
import pandas as pd
import numpy as np

# --- Config ---
WINDOW_SIZE = 96  # 2 days of 30-min bars
STRIDE = 1        # stride for sliding windows

# Directories
ohlcv_dir = os.path.join(os.path.dirname(__file__), "../data_pipeline/cache/ohlcv")
output_dir = os.path.join(os.path.dirname(__file__), "../data_pipeline/cache/price_windows")
os.makedirs(output_dir, exist_ok=True)

def normalize_window(window):
    # log-scale volume before z-score
    window[:, 4] = np.log1p(window[:, 4])  # apply to volume
    return (window - window.mean(axis=0)) / (window.std(axis=0) + 1e-8)

def classify_regime(window):
    # Simple rule-based label: compare first and last close
    close = window[:, 3]  # close is 4th column in OHLCV
    change = close[-1] / close[0] - 1

    if change > 0.02:
        return "trending_up"
    elif change < -0.02:
        return "trending_down"
    elif close.std() < 0.005:
        return "flat"
    else:
        return "volatile"

def process_file(filepath, ticker):
    df = pd.read_csv(filepath, sep=';', parse_dates=['datetime'])
    df = df.sort_values('datetime')
    df.set_index('datetime', inplace=True)  # Set datetime as index here
    
    df = df[["open", "high", "low", "close", "volume"]].values

    X = []
    y = []
    timestamps = []

    for i in range(0, len(df) - WINDOW_SIZE, STRIDE):
        window = df[i:i+WINDOW_SIZE]
        norm_window = normalize_window(window)
        label = classify_regime(window)
        X.append(norm_window)
        y.append(label)
        timestamps.append(i + WINDOW_SIZE - 1)

    return np.array(X), y, timestamps

# Process all tickers
for fname in os.listdir(ohlcv_dir):
    if not fname.endswith(".csv"):
        continue

    ticker = fname.replace(".csv", "")
    filepath = os.path.join(ohlcv_dir, fname)

    try:
        X, y, ts = process_file(filepath, ticker)

        np.save(os.path.join(output_dir, f"{ticker}_X.npy"), X)
        pd.DataFrame({"timestamp_index": ts, "label": y}).to_csv(
            os.path.join(output_dir, f"{ticker}_labels.csv"), index=False
        )

        print(f"{ticker}: {len(X)} windows processed.")
    except Exception as e:
        print(f"Error processing {ticker}: {e}")
