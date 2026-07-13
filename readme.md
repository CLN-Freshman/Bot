# Telegram Bot on Vercel

A simple Telegram bot deployed on Vercel using Python and python-telegram-bot.

## Setup Instructions

### 1. Create a Telegram Bot
- Open Telegram and search for @BotFather
- Send `/newbot` and follow the instructions
- Copy the bot token you receive

### 2. Deploy on Vercel

1. Fork this repository
2. Go to [Vercel](https://vercel.com) and create a new project
3. Connect your GitHub repository
4. Add the environment variable:
   - `TELEGRAM_TOKEN`: Your bot token from BotFather

### 3. Set Webhook

After deployment, set the webhook URL:
