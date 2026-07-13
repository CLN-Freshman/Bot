from flask import Flask, request, jsonify
import os
import sys

# Create Flask app
app = Flask(__name__)

# Print debug info to logs
print(f"✅ Python version: {sys.version}")
print(f"✅ Current directory: {os.getcwd()}")
print(f"✅ Files: {os.listdir('.')}")
print(f"✅ BOT_TOKEN set: {bool(os.environ.get('BOT_TOKEN'))}")

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "ok",
        "message": "Bot is running!",
        "python_version": sys.version,
        "bot_token_set": bool(os.environ.get('BOT_TOKEN'))
    })

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "bot_token_set": bool(os.environ.get('BOT_TOKEN'))
    })

@app.route('/api/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        print(f"✅ Webhook received: {data}")
        return jsonify({
            "status": "ok",
            "received": True
        }), 200
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# This is what Vercel looks for
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)