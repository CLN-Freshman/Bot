from flask import Flask, jsonify
import os

# Create the Flask app
app = Flask(__name__)  # ← This MUST be named 'app'

@app.route('/')
def home():
    return jsonify({
        "status": "ok",
        "message": "Bot is running"
    })

@app.route('/api/webhook', methods=['POST'])
def webhook():
    return jsonify({"status": "ok"})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "bot_token_set": bool(os.environ.get("BOT_TOKEN"))
    })

# Vercel looks for 'app' - this is already defined above
# No need for handler() function