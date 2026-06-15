import os
import requests
import pandas as pd
import yfinance as yf

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "SBIN.NS",
    "LT.NS",
    "BHARTIARTL.NS",
    "ITC.NS",
    "HINDUNILVR.NS"
]

def calculate_rsi(data, period=14):
    delta = data.diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi

signals = []

for stock in stocks:
    try:

        df = yf.download(
            stock,
            period="6mo",
            progress=False,
            auto_adjust=True
        )

        if len(df) < 60:
            continue

        close = df["Close"]

        ema20 = close.ewm(span=20).mean()
        ema50 = close.ewm(span=50).mean()

        rsi = calculate_rsi(close)

        current_price = float(close.iloc[-1])
        current_ema20 = float(ema20.iloc[-1])
        current_ema50 = float(ema50.iloc[-1])
        current_rsi = float(rsi.iloc[-1])

        if (
            current_price > current_ema20
            and current_ema20 > current_ema50
            and current_rsi > 55
        ):

            stop_loss = round(current_price * 0.95, 2)
            target = round(current_price * 1.10, 2)

            signals.append(
                f"""
📈 BUY ALERT

Stock: {stock}

Entry: ₹{round(current_price,2)}
Stop Loss: ₹{stop_loss}
Target: ₹{target}

RSI: {round(current_rsi,1)}
"""
            )

    except Exception as e:
        print(stock, e)

if signals:
    message = "\n\n====================\n\n".join(signals)
else:
    message = "❌ No Swing Trading Signals Today"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": message[:4000]
    }
)
