import yfinance as yf
yf.Ticker("AAPL").news

news = yf.Ticker("AAPL").get_news(count=100, tab='news')
for item in news:
    print(item)
