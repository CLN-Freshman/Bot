import logging
from telegram import Update
from telegram.ext import ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    welcome_message = (
        f"Hi {user.first_name}! 👋\n\n"
        "I'm a simple Telegram bot running on Vercel!\n"
        "Here are some commands you can try:\n"
        "/start - Show this message\n"
        "/help - Get help\n"
        "/echo <text> - Echo your message\n"
        "/ping - Check if bot is alive"
    )
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_text = (
        "Available commands:\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/echo <text> - Echo your message back\n"
        "/ping - Check bot status\n"
        "/about - About this bot"
    )
    await update.message.reply_text(help_text)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the user message."""
    # Get the text after the /echo command
    if context.args:
        text_to_echo = ' '.join(context.args)
        await update.message.reply_text(f"📢 {text_to_echo}")
    else:
        await update.message.reply_text("Please provide text to echo. Example: /echo Hello World!")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check if the bot is alive."""
    await update.message.reply_text("🏓 Pong! Bot is alive and running on Vercel!")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send information about the bot."""
    about_text = (
        "🤖 Telegram Bot\n"
        "Version: 1.0.0\n"
        "Deployed on: Vercel\n"
        "Framework: python-telegram-bot\n"
        "Made with ❤️ using Python"
    )
    await update.message.reply_text(about_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle non-command messages."""
    message_text = update.message.text
    if message_text:
        await update.message.reply_text(
            f"I received your message: '{message_text}'\n"
            "Use /help to see available commands."
        )