from fredapi import Fred
import pandas as pd
from pathlib import Path
import time

API_KEY = "54d41e91156cda4673c7cb47e3dfb24f"
fred = Fred(api_key=API_KEY)

# Updated indicators with correct FRED series codes
INDICATORS = {
    "fed_funds": "FEDFUNDS",        # Federal Funds Rate
    "10y_yield": "DGS10",           # 10-Year Treasury Constant Maturity Rate
    "2y_yield": "DGS2",             # 2-Year Treasury (more liquid)
    "3m_yield": "DGS3MO",           # 3-Month Treasury
    "cpi": "CPIAUCSL",              # Consumer Price Index
    "unemployment": "UNRATE",       # Unemployment Rate
    "pce": "PCEPI",                 # PCE Price Index (Fed's preferred inflation measure)
    "gdp": "GDP",                   # Gross Domestic Product
    "real_gdp": "GDPC1",            # Real GDP
}

# Note: VIX is not available on FRED - you'll need Yahoo Finance for that
# PMI code "NAPMPI" might be outdated - using ISM Manufacturing PMI instead
INDICATORS["ism_pmi"] = "NAPM"  # ISM Manufacturing PMI

def fetch_macro_indicators():
    """Fetch macro indicators with error handling and retry logic"""
    out = {}
    failed = []
    
    for name, code in INDICATORS.items():
        try:
            print(f"Fetching {name} ({code})...")
            df = fred.get_series(code)
            if df is not None and not df.empty:
                out[name] = df
                print(f"✓ Successfully fetched {name}: {len(df)} observations")
            else:
                print(f"✗ No data returned for {name}")
                failed.append((name, code))
                
        except Exception as e:
            print(f"✗ Failed to fetch {name} ({code}): {str(e)}")
            failed.append((name, code))
            
        # Be nice to FRED API
        time.sleep(0.1)
    
    if failed:
        print(f"\nFailed to fetch {len(failed)} indicators:")
        for name, code in failed:
            print(f"  - {name} ({code})")
    
    return out

def save_all(data_dict):
    """Save all series to CSV files"""
    cache_dir = Path("cache/macro/")
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    for name, series in data_dict.items():
        try:
            df = series.reset_index()
            df.columns = ["date", "value"]
            
            # Add some basic data info
            print(f"Saving {name}: {len(df)} rows, from {df['date'].min()} to {df['date'].max()}")
            
            df.to_csv(cache_dir / f"{name}.csv", index=False)
        except Exception as e:
            print(f"Error saving {name}: {e}")

def get_vix_from_yahoo():
    """Fetch VIX data from Yahoo Finance as FRED doesn't have it"""
    try:
        import yfinance as yf
        vix = yf.download("^VIX", period="max", auto_adjust=True, progress=False)
        return vix['Close'].dropna()
    except ImportError:
        print("yfinance not installed. Run: pip install yfinance")
        return None
    except Exception as e:
        print(f"Error fetching VIX: {e}")
        return None

if __name__ == "__main__":
    print("Fetching FRED data...")
    data = fetch_macro_indicators()
    
    print(f"\nSuccessfully fetched {len(data)} indicators")
    
    # Try to get VIX from Yahoo Finance
    print("\nFetching VIX from Yahoo Finance...")
    vix_data = get_vix_from_yahoo()
    if vix_data is not None:
        data["vix"] = vix_data
        print(f"✓ Successfully fetched VIX: {len(vix_data)} observations")
    
    # Save all data
    print("\nSaving data...")
    save_all(data)
    print("Done!")