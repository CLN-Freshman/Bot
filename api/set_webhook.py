from telegram import Update
import os
import requests
import json

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables!")

# Get the Vercel URL from environment or use the default
VERCEL_URL = os.environ.get("VERCEL_URL", "your-app.vercel.app")
WEBHOOK_URL = f"https://{VERCEL_URL}/api/webhook"

def set_webhook():
    """Set the webhook for the bot."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    payload = {
        "url": WEBHOOK_URL,
        "allowed_updates": ["message", "callback_query"]
    }
    
    response = requests.post(url, json=payload)
    result = response.json()
    
    if result.get("ok"):
        print(f"✅ Webhook set successfully to: {WEBHOOK_URL}")
    else:
        print(f"❌ Failed to set webhook: {result}")
    
    return result

if __name__ == "__main__":
    set_webhook()