from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ============================================================
# 🔑 Read tokens from environment variables
# ============================================================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEB_APP_URL = os.environ.get("WEB_APP_URL", "https://your-frontend-app.vercel.app/")

logger.info(f"BOT_TOKEN set: {bool(BOT_TOKEN)}")
logger.info(f"WEB_APP_URL: {WEB_APP_URL}")

# ============================================================
# Bot Commands
# ============================================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message when /start is issued."""
    if not BOT_TOKEN:
        await update.message.reply_text("⚠️ Bot is not properly configured.")
        return
    
    web_app_button = InlineKeyboardButton(
        "🚀 Open Web App", 
        web_app=WebAppInfo(url=WEB_APP_URL)
    )
    reply_markup = InlineKeyboardMarkup([[web_app_button]])
    
    welcome_text = (
        "👋 Welcome to Our Bot!\n\n"
        "We're excited to have you here. "
        "Click the button below to explore our powerful web app.\n\n"
        "✨ Features include:\n"
        "• Interactive dashboard\n"
        "• Real-time updates\n"
        "• And much more!"
    )
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a help message when /help is issued."""
    help_text = (
        "🤖 Available Commands:\n"
        "/start - Welcome message with Web App link\n"
        "/help - Show this help message\n"
        "/about - Learn more about us"
    )
    await update.message.reply_text(help_text)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send an about message when /about is issued."""
    about_text = (
        "ℹ️ About This Bot\n\n"
        "This bot connects you to our innovative Web App. "
        "Built with ❤️ using Telegram's Mini App platform.\n\n"
        "📱 Open the Web App to access all features!"
    )
    await update.message.reply_text(about_text)

# ============================================================
# Routes
# ============================================================

@app.route('/', methods=['GET'])
def index():
    """Root endpoint to check if bot is running."""
    return jsonify({
        "status": "running" if BOT_TOKEN else "error",
        "message": "Bot is active!" if BOT_TOKEN else "Bot token not configured!",
        "webhook": "/api/webhook",
        "bot_token_set": bool(BOT_TOKEN),
        "web_app_url": WEB_APP_URL
    })

@app.route('/api/webhook', methods=['POST'])
async def webhook():
    """Handle incoming webhook requests."""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not configured!")
        return jsonify({"status": "error", "message": "Bot token not configured"}), 500
    
    try:
        data = request.get_json()
        
        if not data:
            logger.warning("No data received")
            return jsonify({"status": "error", "message": "No data received"}), 400
        
        logger.info("Received webhook update")
        
        # Create the Application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Register command handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("about", about_command))
        
        # Process the update
        await application.process_update(Update.de_json(data, application.bot))
        
        logger.info("Webhook processed successfully")
        return jsonify({"status": "ok"}), 200
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "bot_token_set": bool(BOT_TOKEN),
        "web_app_url": WEB_APP_URL
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)