from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import json

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables!")

WEB_APP_URL = os.environ.get("WEB_APP_URL")
if not WEB_APP_URL:
    raise ValueError("No WEB_APP_URL found in environment variables!")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message when /start is issued."""
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

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "running",
        "message": "Bot is active!",
        "webhook": "/api/webhook"
    })

@app.route('/api/webhook', methods=['POST'])
async def webhook():
    """Handle incoming webhook requests."""
    try:
        # Get the request body
        data = request.get_json()
        
        # Create the Application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Register command handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("about", about_command))
        
        # Process the update
        await application.process_update(Update.de_json(data, application.bot))
        
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)