import requests

BOT_TOKEN ="8809597527:AAHVVTVw6fTBWvjF4qmVpFKtAzyqukXJ56A"
CHAT_ID = "799554389"

message = "Test Message From Trading Bot"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)
