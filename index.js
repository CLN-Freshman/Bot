const express = require('express');
const { Telegraf } = require('telegraf');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

// Initialize bot with token
const bot = new Telegraf(process.env.BOT_TOKEN);

const WEBAPP_URL = process.env.WEBAPP_URL;

// Bot commands
bot.command('start', (ctx) => {
  console.log('Start command received from:', ctx.from.username || ctx.from.id);
  
  const welcomeMessage = `👋 Welcome to Our Bot!

We're excited to have you here. Click the button below to explore our powerful web app.

✨ Features include:
• Interactive dashboard
• Real-time updates
• And much more`;

  ctx.reply(welcomeMessage, {
    reply_markup: {
      inline_keyboard: [
        [
          {
            text: '🚀 Open Web App',
            web_app: {
              url: WEBAPP_URL
            }
          }
        ],
        [
          {
            text: '❓ Help',
            callback_data: 'help'
          }
        ]
      ]
    }
  }).catch(err => {
    console.error('Error sending start message:', err);
  });
});

// Handle callback queries
bot.action('help', (ctx) => {
  ctx.answerCbQuery();
  ctx.reply('Available commands:\n/start - Start the bot\n/help - Show this help\n/ping - Check if bot is alive\n/echo <text> - Echo your message\n/open - Open the web app');
});

bot.command('help', (ctx) => {
  ctx.reply('Available commands:\n/start - Start the bot\n/help - Show this help\n/ping - Check if bot is alive\n/echo <text> - Echo your message\n/open - Open the web app');
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

// Command to open web app
bot.command('open', (ctx) => {
  ctx.reply('Click the button below to open the web app:', {
    reply_markup: {
      inline_keyboard: [
        [
          {
            text: '🚀 Open Web App',
            web_app: {
              url: WEBAPP_URL
            }
          }
        ]
      ]
    }
  });
});

// Handle any text message
bot.on('text', (ctx) => {
  ctx.reply(`You said: ${ctx.message.text}`);
});

// Webhook endpoint for Vercel - FIXED VERSION
app.use(express.json());

app.post('/webhook', async (req, res) => {
  try {
    console.log('Webhook received:', req.body.message?.text || 'No text');
    await bot.handleUpdate(req.body);
    res.sendStatus(200);
  } catch (error) {
    console.error('Error handling webhook:', error);
    res.sendStatus(500);
  }
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