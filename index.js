const express = require('express');
const { Telegraf } = require('telegraf');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

// Initialize bot with token
const bot = new Telegraf(process.env.BOT_TOKEN);

// Bot commands
bot.command('start', (ctx) => {
  ctx.reply('Welcome! I am your Telegram bot. Here are the commands:\n/help - Show help\n/ping - Check if bot is alive\n/echo <text> - Echo your message');
});

bot.command('help', (ctx) => {
  ctx.reply('Available commands:\n/start - Start the bot\n/help - Show this help\n/ping - Check if bot is alive\n/echo <text> - Echo your message');
});

bot.command('ping', (ctx) => {
  ctx.reply('Pong! 🏓');
});

bot.command('echo', (ctx) => {
  const text = ctx.message.text.split(' ').slice(1).join(' ');
  if (!text) {
    ctx.reply('Please provide text to echo. Example: /echo Hello World');
    return;
  }
  ctx.reply(text);
});

// Handle any text message
bot.on('text', (ctx) => {
  ctx.reply(`You said: ${ctx.message.text}`);
});

// Webhook endpoint for Vercel
app.use(express.json());
app.post('/webhook', (req, res) => {
  bot.handleUpdate(req.body, res);
});

// Health check endpoint
app.get('/', (req, res) => {
  res.send('Bot is running!');
});

// Export app for Vercel
module.exports = app;

// For local development
if (process.env.NODE_ENV !== 'production') {
  app.listen(port, () => {
    console.log(`Bot running on port ${port}`);
    
    // For local development, use polling
    bot.launch();
    console.log('Bot started with polling');
  });
}