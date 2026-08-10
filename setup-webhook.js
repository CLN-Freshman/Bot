const { Telegraf } = require('telegraf');
require('dotenv').config();

const bot = new Telegraf(process.env.BOT_TOKEN);

const WEBHOOK_URL = process.env.WEBHOOK_URL;

async function setupWebhook() {
  try {
    await bot.telegram.deleteWebhook();
    console.log('Existing webhook deleted');
    
    const result = await bot.telegram.setWebhook(WEBHOOK_URL);
    console.log('Webhook set successfully!', result);
    
    const info = await bot.telegram.getWebhookInfo();
    console.log('Webhook info:', JSON.stringify(info, null, 2));
  } catch (err) {
    console.error('Error setting webhook:', err.message);
  }
}

setupWebhook();