import os
import requests
import yfinance as yf

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

stock = "RELIANCE.NS"

df = yf.download(
    stock,
    period="5d",
    progress=False,
    auto_adjust=True
)

close_price = round(float(df["Close"].values[-1]), 2)

message = f"""
✅ YFinance Working

Stock: RELIANCE
Current Price: ₹{close_price}
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)
