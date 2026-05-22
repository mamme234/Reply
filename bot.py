import os
import asyncio
import threading
from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ================= CONFIG =================

TOKEN = os.getenv("BOT_TOKEN")

# Your personal Telegram ID
ADMIN_ID = 7154361039

# ================= FLASK =================

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running successfully!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    welcome_message = f"""
✨ Welcome ꧁ɪ ᴀᴍ Tᕼᗴ KIᑎᘜ꧂ ✨

Thank you for messaging me 🤍

Send your message or problem here.

━━━━━━━━━━━━━━━

✨ እንኳን ደህና መጡ ✨

መልእክትዎን ስላደረሱልኝ እናመሰግናለን 🤍

ችግርዎን ወይም መልእክትዎን ይላኩ።

━━━━━━━━━━━━━━━

✨ Baga nagaan dhuftan ✨

Ergaa keessaniif galatoomaa 🤍

Rakkoo keessan as irratti naaf ergaa.
"""

    await update.message.reply_text(welcome_message)

# ================= MESSAGE HANDLER =================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    text = update.message.text

    # ================= LUXURY PERSONAL REPLY =================

    luxury_reply = f"""
✨ Welcome ꧁ɪ ᴀᴍ Tᕼᗴ KIᑎᘜ꧂ ✨

Thank you for your message 🤍

I’m currently offline and out for personal business right now.

If you need support, send your problem clearly and I’ll check it once I’m available.

📞 For urgent matters:
+251934600018

⏳ Please be patient, I’ll reply as soon as possible.

━━━━━━━━━━━━━━━

✨ እንኳን ደህና መጡ ✨

መልእክትዎን ስላደረሱልኝ እናመሰግናለን 🤍

አሁን በግል ስራ ላይ ስለሆንኩ ከመስመር ውጭ ነኝ።

ችግርዎን በግልፅ ይላኩልኝ፣ ሲመቸኝ እመለከተዋለሁ።

📞 አስቸኳይ ከሆነ:
+251934600018

⏳ እባክዎ ትዕግስት ያድርጉ።

━━━━━━━━━━━━━━━

✨ Baga nagaan dhuftan ✨

Ergaa naaf ergitaniif galatoomaa 🤍

Amma hojii dhuunfaa irratti waanan jiruuf online miti.

Rakkoo keessan ifatti naaf barreessaa, yeroo argadhetti nan ilaala.

📞 Yoo ariifachiisaa ta’e:
+251934600018

⏳ Obsaan eegaa, deebii nan kenna.
"""

    # reply to user (acts like YOU speaking)
    await update.message.reply_text(luxury_reply)

    # send to your personal Telegram account
    admin_message = f"""
📩 New Message

👤 Name: {user.first_name}
🆔 ID: {user.id}
📨 Username: @{user.username}

━━━━━━━━━━━━━━━

💬 Message:
{text}
"""

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=admin_message
    )

# ================= MAIN =================

async def main():

    bot_app = Application.builder().token(TOKEN).build()

    bot_app.add_handler(CommandHandler("start", start))

    bot_app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("Bot started successfully...")

    await bot_app.initialize()
    await bot_app.start()
    await bot_app.updater.start_polling()

    while True:
        await asyncio.sleep(100)

# ================= RUN =================

if __name__ == "__main__":

    threading.Thread(target=run_web).start()
    asyncio.run(main())
