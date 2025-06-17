# import yfinance as yf
# import pandas as pd
# from pathlib import Path
# from datetime import datetime
# from time import sleep

# TICKER_FILE = Path("cache/tickers.csv")
# NEWS_DIR = Path("cache/news")
# NEWS_DIR.mkdir(parents=True, exist_ok=True)

# def parse_article(article):
#     try:
#         content = article.get("content", {})
#         pub_date = content.get("pubDate")
#         title = content.get("title", "")
#         publisher = content.get("provider", {}).get("displayName", "")
#         url = content.get("clickThroughUrl", {}).get("url") or \
#               content.get("canonicalUrl", {}).get("url")

#         return {
#             "timestamp": pd.to_datetime(pub_date),
#             "title": title,
#             "publisher": publisher,
#             "link": url
#         }
#     except Exception as e:
#         print(f"⚠️ Failed to parse article: {e}")
#         return None

# def fetch_news(ticker):
#     try:
#         print(f"\n🔎 Fetching news for: {ticker}")
#         t = yf.Ticker(ticker)
#         news_list = t.news

#         if not news_list:
#             print("⚠️ No news found")
#             return pd.DataFrame()

#         parsed = [parse_article(item) for item in news_list]
#         parsed = [p for p in parsed if p is not None]
#         return pd.DataFrame(parsed)

#     except Exception as e:
#         print(f"❌ Error fetching news for {ticker}: {e}")
#         return pd.DataFrame()

# def save_news(ticker, df):
#     if df.empty:
#         print(f"⚠️ No articles to save for {ticker}")
#         return
#     path = NEWS_DIR / f"{ticker.upper()}.csv"
#     if path.exists():
#         old = pd.read_csv(path, parse_dates=["timestamp"])
#         df = pd.concat([old, df]).drop_duplicates("title").sort_values("timestamp")
#     df.to_csv(path, index=False)
#     print(f"💾 Saved {len(df)} articles to {path}")

# if __name__ == "__main__":
#     df_tickers = pd.read_csv(TICKER_FILE)
#     tickers = df_tickers["Ticker"].dropna().unique().tolist()[:10]

#     for ticker in tickers:
#         df_news = fetch_news(ticker)
#         save_news(ticker, df_news)
#         sleep(1)  # Be polite to the API


import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime
from time import sleep

TICKER_FILE = Path("cache/tickers.csv")
NEWS_DIR = Path("cache/news")
NEWS_DIR.mkdir(parents=True, exist_ok=True)

def parse_article(article):
    try:
        content = article.get("content", {})
        pub_date = content.get("pubDate")
        title = content.get("title", "")
        publisher = content.get("provider", {}).get("displayName", "")
        url = content.get("clickThroughUrl", {}).get("url") or \
              content.get("canonicalUrl", {}).get("url")

        return {
            "timestamp": pd.to_datetime(pub_date),
            "title": title,
            "publisher": publisher,
            "link": url
        }
    except Exception as e:
        print(f"⚠️ Failed to parse article: {e}")
        return None

def fetch_news(ticker):
    try:
        print(f"\n🔎 Fetching news for: {ticker}")
        t = yf.Ticker(ticker)
        news_list = t.get_news(count=10000, tab="news")

        if not news_list:
            print("⚠️ No news found")
            return pd.DataFrame()

        parsed = [parse_article(item) for item in news_list]
        parsed = [p for p in parsed if p is not None]
        return pd.DataFrame(parsed)

    except Exception as e:
        print(f"❌ Error fetching news for {ticker}: {e}")
        return pd.DataFrame()

def save_news(ticker, df):
    if df.empty:
        print(f"⚠️ No articles to save for {ticker}")
        return
    path = NEWS_DIR / f"{ticker.upper()}.csv"
    if path.exists():
        old = pd.read_csv(path, parse_dates=["timestamp"])
        df = pd.concat([old, df]).drop_duplicates("title").sort_values("timestamp")
    df.to_csv(path, index=False)
    print(f"💾 Saved {len(df)} articles to {path}")

if __name__ == "__main__":
    df_tickers = pd.read_csv(TICKER_FILE)
    tickers = df_tickers["Ticker"].dropna().unique().tolist()[:10]

    for ticker in tickers:
        df_news = fetch_news(ticker)
        save_news(ticker, df_news)
        sleep(1)  # Be polite to Yahoo servers
