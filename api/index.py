from flask import Flask, request, jsonify
import os
import sys
import json

# Create Flask app - MUST be named 'app'
app = Flask(__name__)

# Debug info (visible in Vercel logs)
print(f"✅ Python version: {sys.version}", file=sys.stderr)
print(f"✅ Flask app created successfully", file=sys.stderr)

# Environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEB_APP_URL = os.environ.get("WEB_APP_URL", "https://your-frontend.vercel.app/")

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "ok",
        "message": "Bot is running!",
        "bot_token_set": bool(BOT_TOKEN),
        "python_version": sys.version
    })

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "bot_token_set": bool(BOT_TOKEN),
        "web_app_url": WEB_APP_URL
    })

@app.route('/api/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        print(f"✅ Webhook received: {data}", file=sys.stderr)
        
        # Simple response
        return jsonify({
            "status": "ok",
            "received": True
        }), 200
    except Exception as e:
        print(f"❌ Webhook error: {e}", file=sys.stderr)
        return jsonify({"status": "error", "message": str(e)}), 500

# Optional: Add error handler
@app.errorhandler(404)
def not_found(e):
    return jsonify({"status": "error", "message": "Not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"status": "error", "message": "Server error"}), 500