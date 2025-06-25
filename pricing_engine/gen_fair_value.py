import os
import pandas as pd
from datetime import datetime, timezone
from asset_models import black_scholes_price

# --- Config ---
BASE_DIR = os.path.dirname(__file__)
option_dir = os.path.join(BASE_DIR, "../data_pipeline/cache/current_option_chain")
output_dir = os.path.join(BASE_DIR, "fair_value")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "fair_values.csv")
today = datetime.now(timezone.utc)

# --- Load risk-free rate ---
macro_path = os.path.join(BASE_DIR, "../data_pipeline/cache/macro/3m_yield.csv")
df_yield = pd.read_csv(macro_path)
r = df_yield.iloc[-1]['value']

# --- Load tickers ---
tickers_path = os.path.join(BASE_DIR, "../data_pipeline/cache/tickers.csv")
tickers_df = pd.read_csv(tickers_path)
tickers_to_run = tickers_df["Ticker"].head(10).tolist()

records = []

# --- Loop over option chain files ---
for filename in os.listdir(option_dir):
    if not filename.endswith("_options.csv"):
        continue

    ticker = filename.split("_")[0]
    if ticker not in tickers_to_run:
        continue

    filepath = os.path.join(option_dir, filename)

    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        print(f"Failed to read {filename}: {e}")
        continue

    # Load OHLCV (semicolon-delimited)
    ohlcv_path = os.path.join(BASE_DIR, f"../data_pipeline/cache/ohlcv/{ticker}_OHLCV.csv")
    try:
        df_ohlcv = pd.read_csv(ohlcv_path, delimiter=';')
        df_ohlcv["datetime"] = pd.to_datetime(df_ohlcv["datetime"])
        df_ohlcv.sort_values("datetime", inplace=True)
        S = df_ohlcv.iloc[-1]['close']
    except Exception as e:
        print(f"Failed to read OHLCV for {ticker}: {e}")
        continue

    for _, row in df.iterrows():
        try:
            K = float(row["strike"])
            option_type = 'C' if str(row["type"]).lower() == "call" else 'P'
            expiration = pd.to_datetime(row["expirationDate"], utc=True)
            T = (expiration - today).days / 365.0

            sigma = float(row["impliedVolatility"])
            bid, ask = float(row["bid"]), float(row["ask"])
            market_price = (bid + ask) / 2

            if T <= 0 or sigma <= 0 or market_price <= 0:
                continue

            fair_value = black_scholes_price(option_type, S, K, T, r, sigma)
            mispricing = market_price - fair_value

            records.append({
                "timestamp": today.isoformat(),
                "ticker": ticker,
                "strike": K,
                "type": option_type,
                "market_price": round(market_price, 2),
                "fair_value": round(fair_value, 2),
                "mispricing": round(mispricing, 2)
            })
        except Exception as e:
            print(f"Error processing option for {ticker}: {e}")

# --- Save output ---
fair_df = pd.DataFrame(records)
fair_df.to_csv(output_path, index=False)
print(f"Saved fair_values.csv with {len(fair_df)} entries.")
