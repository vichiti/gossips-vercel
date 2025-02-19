import os
import requests
from fastapi import FastAPI, Request

# Get environment variables
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Google Cloud Run URL

app = FastAPI()

@app.on_event("startup")
async def set_webhook():
    """Set Telegram webhook on bot startup"""
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}"
    requests.get(url)

@app.post("/webhook")
async def webhook(request: Request):
    """Handle incoming Telegram messages"""
    data = await request.json()
    chat_id = data.get("message", {}).get("chat", {}).get("id")
    text = data.get("message", {}).get("text", "").strip()

    if text == "/start":
        send_message(chat_id, "Welcome! 🚀 Running on Google Cloud Run.")
    elif text == "/help":
        send_message(chat_id, "This bot auto-scales with Cloud Run!")
    
    return {"status": "ok"}

def send_message(chat_id, text):
    """Send a message via Telegram API"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.get("/")
def home():
    return {"status": "Bot is running on Cloud Run"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
