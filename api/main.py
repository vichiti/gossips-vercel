import os
import requests
from fastapi import FastAPI, Request
from mangum import Mangum  # ✅ Required for Vercel compatibility

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Set this to your Vercel deployment URL

app = FastAPI()

@app.on_event("startup")
async def set_webhook():
    """Set the webhook on Telegram bot startup"""
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}"
    requests.get(url)

@app.post("/webhook")
async def webhook(request: Request):
    """Handle incoming messages from Telegram"""
    data = await request.json()
    chat_id = data.get("message", {}).get("chat", {}).get("id")
    text = data.get("message", {}).get("text", "").strip()

    if text == "/start":
        send_message(chat_id, "Welcome! 🚀 Running on Vercel.")
    elif text == "/help":
        send_message(chat_id, "This bot auto-scales with Vercel serverless functions!")

    return {"status": "ok"}

def send_message(chat_id, text):
    """Send a message via Telegram API"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.get("/")
def home():
    return {"status": "Bot is running on Vercel with fastapi"}

# ✅ Use Mangum to make FastAPI work with Vercel
handler = Mangum(app)
