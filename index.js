const express = require('express');
const { Telegraf } = require('telegraf');
const { createClient } = require('@supabase/supabase-js');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

const bot = new Telegraf(process.env.BOT_TOKEN);

const WEBAPP_URL =
  process.env.WEBAPP_URL || 'https://cln-freshmen.vercel.app/';

const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_KEY;

if (!process.env.BOT_TOKEN) {
  console.error('❌ BOT_TOKEN is missing');
}

if (!SUPABASE_URL || !SUPABASE_KEY) {
  console.error('❌ SUPABASE_URL or SUPABASE_KEY is missing');
}

const supabase = createClient(
  SUPABASE_URL,
  SUPABASE_KEY
);

function makeHashtag(value) {
  if (!value) return '';

  return (
    '#' +
    String(value)
      .trim()
      .replace(/[^a-zA-Z0-9_]+/g, '')
  );
}

function formatDate(date) {
  if (!date) return '';

  return new Date(date).toLocaleString('en-US', {
    dateStyle: 'medium',
    timeStyle: 'short'
  });
}

// Format one announcement for Telegram
function formatAnnouncement(announcement) {
  const category = makeHashtag(announcement.category);
  const priority = makeHashtag(announcement.priority);

  const hashtags = [category, priority]
    .filter(Boolean)
    .join(' ');

  const pinned = announcement.is_pinned
    ? '📌 PINNED\n\n'
    : '';

  const createdDate = formatDate(announcement.created_at);
  return `${pinned}📢 <b>${escapeHtml(announcement.title || 'Announcement')}</b>

${escapeHtml(announcement.content || '')}

${hashtags}
🕒 ${createdDate}`;
}

// Escape HTML for Telegram
function escapeHtml(text) {
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

async function getAnnouncements() {
  const { data, error } = await supabase
    .from('announcements')
    .select(`
      id,
      title,
      content,
      category,
      priority,
      is_pinned,
      is_published,
      created_at,
      published_at,
      expires_at,
      views,
      likes,
      comments,
      shares,
      target_audience,
      image_url
    `)
    .eq('is_published', true);

  if (error) {
    console.error('❌ Supabase error:', error);
    throw error;
  }

  const announcements = data || [];

  announcements.sort((a, b) => {
    const dateA = new Date(a.published_at || a.created_at);
    const dateB = new Date(b.published_at || b.created_at);

    return dateA.getTime() - dateB.getTime();
  });

  return announcements;
}

bot.command('announcements', async (ctx) => {
  try {
    console.log(
      'Announcements requested by:',
      ctx.from.username || ctx.from.id
    );

    await ctx.reply('📢 Fetching announcements...');

    const announcements = await getAnnouncements();

    if (announcements.length === 0) {
      await ctx.reply(
        '📭 There are no published announcements right now.'
      );
      return;
    }

    for (const announcement of announcements) {
      const message = formatAnnouncement(announcement);
      if (message.length <= 4096) {
let sentMessage;

if (announcement.image_url) {
  sentMessage = await ctx.replyWithPhoto(
    {
      url: announcement.image_url
    },
    {
      caption: message,
      parse_mode: 'HTML'
    }
  );
} else {
  sentMessage = await ctx.reply(message, {
    parse_mode: 'HTML',
    disable_web_page_preview: true
  });
}

        if (announcement.is_pinned) {
          try {
            await ctx.telegram.pinChatMessage(
              ctx.chat.id,
              sentMessage.message_id,
              {
                disable_notification: true
              }
            );

            console.log(
              `📌 Pinned announcement ${announcement.id}`
            );
          } catch (pinError) {
            console.error(
              `⚠️ Could not pin announcement ${announcement.id}:`,
              pinError.message
            );
          }
        }
      } else {
        const chunks = splitMessage(message, 4096);

        let firstMessage = null;

        for (const chunk of chunks) {
          const sentMessage = await ctx.reply(chunk, {
            parse_mode: 'HTML',
            disable_web_page_preview: true
          });

          if (!firstMessage) {
            firstMessage = sentMessage;
          }
        }

        if (announcement.is_pinned && firstMessage) {
          try {
            await ctx.telegram.pinChatMessage(
              ctx.chat.id,
              firstMessage.message_id,
              {
                disable_notification: true
              }
            );
          } catch (pinError) {
            console.error(
              '⚠️ Could not pin long announcement:',
              pinError.message
            );
          }
        }
      }
    }

  } catch (error) {
    console.error('❌ Error fetching announcements:', error);

    await ctx.reply(
      '❌ Sorry, I could not fetch the announcements right now.'
    );
  }
});

function splitMessage(text, maxLength) {
  const chunks = [];

  for (let i = 0; i < text.length; i += maxLength) {
    chunks.push(text.substring(i, i + maxLength));
  }

  return chunks;
}

// ============================================================
// START
// ============================================================

bot.command('start', (ctx) => {
  console.log(
    'Start command received from:',
    ctx.from.username || ctx.from.id
  );

  const welcomeMessage = `👋 Welcome to Our Bot!

We're excited to have you here. Click the button below to explore our powerful web app.

✨ Features include:
• Interactive dashboard
• Real-time updates
• Announcements`;

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
            text: '📢 Announcements',
            callback_data: 'announcements'
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

// ============================================================
// CALLBACK QUERIES
// ============================================================

bot.action('help', async (ctx) => {
  await ctx.answerCbQuery();

  await ctx.reply(
    `Available commands:

/start - Start the bot
/help - Show this help
/ping - Check if bot is alive
/echo <text> - Echo your message
/open - Open the web app
/announcements - View published announcements`
  );
});

bot.action('announcements', async (ctx) => {
  await ctx.answerCbQuery();

  try {
    const announcements = await getAnnouncements();

    if (announcements.length === 0) {
      await ctx.reply(
        '📭 There are no published announcements right now.'
      );
      return;
    }

    for (const announcement of announcements) {
      const message = formatAnnouncement(announcement);

      if (message.length <= 4096) {
        const sentMessage = await ctx.reply(message, {
          parse_mode: 'HTML',
          disable_web_page_preview: true
        });

        if (announcement.is_pinned) {
          try {
            await ctx.telegram.pinChatMessage(
              ctx.chat.id,
              sentMessage.message_id,
              {
                disable_notification: true
              }
            );
          } catch (pinError) {
            console.error(
              'Could not pin announcement:',
              pinError.message
            );
          }
        }
      }
    }

  } catch (error) {
    console.error(error);

    await ctx.reply(
      '❌ Could not load announcements.'
    );
  }
});

// ============================================================
// HELP
// ============================================================

bot.command('help', (ctx) => {
  ctx.reply(
    `Available commands:

/start - Start the bot
/help - Show this help
/ping - Check if bot is alive
/echo <text> - Echo your message
/open - Open the web app
/announcements - View published announcements`
  );
});

// ============================================================
// PING
// ============================================================

bot.command('ping', (ctx) => {
  ctx.reply('Pong! 🏓');
});

// ============================================================
// ECHO
// ============================================================

bot.command('echo', (ctx) => {
  const text = ctx.message.text
    .split(' ')
    .slice(1)
    .join(' ');

  if (!text) {
    ctx.reply(
      'Please provide text to echo. Example: /echo Hello World'
    );
    return;
  }

  ctx.reply(text);
});

// ============================================================
// OPEN WEB APP
// ============================================================

bot.command('open', (ctx) => {
  ctx.reply(
    'Click the button below to open the web app:',
    {
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
    }
  );
});

// ============================================================
// HANDLE TEXT
// ============================================================

bot.on('text', (ctx) => {
  // Don't respond to commands here
  if (ctx.message.text.startsWith('/')) {
    return;
  }

  ctx.reply(
    `You said: ${ctx.message.text}`
  );
});

// ============================================================
// WEBHOOK
// ============================================================

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

    bot.launch();
    console.log('Bot started with polling');
  });
}