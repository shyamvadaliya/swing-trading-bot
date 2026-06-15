import requests
import yfinance as yf

BOT_TOKEN ="8809597527:AAHVVTVw6fTBWvjF4qmVpFKtAzyqukXJ56A"
CHAT_ID = "799554389"

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS"
]

signals = []

for stock in stocks:
    try:
        df = yf.download(stock, period="3mo", progress=False)

        if len(df) < 60:
            continue

        close = float(df["Close"].iloc[-1])
        sma20 = float(df["Close"].rolling(20).mean().iloc[-1])
        sma50 = float(df["Close"].rolling(50).mean().iloc[-1])

        if sma20 > sma50 and close > sma20:
            signals.append(f"BUY: {stock} | Price: ₹{round(close,2)}")

    except Exception:
        pass

if signals:
    message = "📈 Swing Trading Signals\n\n" + "\n".join(signals)
else:
    message = "No Swing Trading Signals Today"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)
