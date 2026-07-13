import os
import json
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import handlers
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bot.handlers import start, help_command, echo, ping, about, handle_message

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment
TOKEN = os.getenv('TELEGRAM_TOKEN')

if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN environment variable is not set!")

# Create application
application = Application.builder().token(TOKEN).build()

# Add command handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("echo", echo))
application.add_handler(CommandHandler("ping", ping))
application.add_handler(CommandHandler("about", about))

# Add message handler for non-command messages
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

async def webhook(request):
    """Handle incoming webhook requests."""
    try:
        # Get the update from the request
        if request.method == 'POST':
            # Parse the request body
            body = await request.body()
            data = json.loads(body.decode('utf-8'))
            
            # Create Update object
            update = Update.de_json(data, application.bot)
            
            # Process the update
            await application.process_update(update)
            
            # Return success response
            return {
                'statusCode': 200,
                'body': 'OK'
            }
        else:
            # Handle GET request - return bot info
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Telegram bot is running!',
                    'status': 'active'
                })
            }
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# Handle different Vercel runtime versions
def handler(request, *args, **kwargs):
    """Wrapper for Vercel serverless function."""
    import asyncio
    return asyncio.run(webhook(request))

# For Vercel Python runtime
async def main(request):
    """Main entry point for Vercel."""
    return await webhook(request)