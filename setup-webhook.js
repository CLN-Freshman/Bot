// Create a separate script called setup-webhook.js
const { Telegraf } = require('telegraf');
require('dotenv').config();

const bot = new Telegraf(process.env.BOT_TOKEN);

const WEBHOOK_URL = 'https://your-app.vercel.app/webhook';

bot.telegram.setWebhook(WEBHOOK_URL).then(() => {
  console.log('Webhook set successfully!');
}).catch(err => {
  console.error('Error setting webhook:', err);
});