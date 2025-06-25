import os
import pandas as pd

# Paths
base_dir = os.path.dirname(__file__)
fair_value_path = os.path.join(base_dir, "../pricing_engine/fair_value/fair_values.csv")
sentiment_dir = os.path.join(base_dir, "../data_pipeline/cache/sentiment")
volatility_dir = os.path.join(base_dir, "../data_pipeline/cache/volatility")
output_path = os.path.join(base_dir, "signals.csv")

# Load fair value data
fair_df = pd.read_csv(fair_value_path, parse_dates=["timestamp"])

# Helper to load sentiment and volatility data
def get_sentiment(ticker, ts):
    path = os.path.join(sentiment_dir, f"{ticker}_sentiment_score.csv")
    if not os.path.exists(path):
        return "Neutral"
    df = pd.read_csv(path, parse_dates=["timestamp"])
    df["timestamp"] = df["timestamp"].dt.tz_localize(None)
    ts = ts.tz_localize(None)
    closest = df.iloc[(df["timestamp"] - ts).abs().argsort()[:1]]
    return closest["label"].values[0]

def get_volatility(ticker, ts):
    path = os.path.join(volatility_dir, f"{ticker}_OHLCV_volatility.csv")
    if not os.path.exists(path):
        return 0.5
    df = pd.read_csv(path, parse_dates=["datetime"])
    df["datetime"] = df["datetime"].dt.tz_localize(None)
    ts = ts.tz_localize(None)
    closest = df.iloc[(df["datetime"] - ts).abs().argsort()[:1]]
    return closest["volatility"].values[0]

# Decision logic
def generate_action(mispricing, sentiment, vol):
    if mispricing < -2 and sentiment == "Bullish" and vol < 0.3:
        return "BUY"
    elif mispricing > 2 and sentiment == "Bearish" and vol > 0.5:
        return "SELL"
    else:
        return "HOLD"

# Process
signals = []
for _, row in fair_df.iterrows():
    ts = pd.to_datetime(row["timestamp"])
    ticker = row["ticker"]
    sentiment = get_sentiment(ticker, ts)
    vol = get_volatility(ticker, ts)
    action = generate_action(row["mispricing"], sentiment, vol)
    
    signals.append({
        "timestamp": ts.isoformat(),
        "ticker": ticker,
        "action": action
    })

# Save
signals_df = pd.DataFrame(signals)
signals_df.to_csv(output_path, index=False)
print(f"Saved signals to {output_path}")
