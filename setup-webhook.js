const { Telegraf } = require('telegraf');
require('dotenv').config();

const bot = new Telegraf(process.env.BOT_TOKEN);

// Make sure this URL is exactly correct
const WEBHOOK_URL = 'https://cln-bot-lilac.vercel.app/webhook';

async function setupWebhook() {
  try {
    // First, delete any existing webhook
    await bot.telegram.deleteWebhook();
    console.log('Existing webhook deleted');
    
    // Set the new webhook
    const result = await bot.telegram.setWebhook(WEBHOOK_URL);
    console.log('Webhook set successfully!', result);
    
    // Verify it was set correctly
    const info = await bot.telegram.getWebhookInfo();
    console.log('Webhook info:', JSON.stringify(info, null, 2));
  } catch (err) {
    console.error('Error setting webhook:', err.message);
  }
}

setupWebhook();