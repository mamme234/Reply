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

# Your Telegram ID
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
✨ Welcome {update.effective_user.first_name} ✨

This is my personal assistant bot 🤍

Send any message and I will receive it directly.

━━━━━━━━━━━━━━━

✨ እንኳን ደህና መጡ ✨

ይህ የግል ረዳት ቦት ነው 🤍

ማንኛውንም መልእክት ይላኩ እኔ በቀጥታ እቀበላለሁ።

━━━━━━━━━━━━━━━

✨ Baga nagaan dhuftan ✨

Kun bot gargaaraa koo dhuunfaa dha 🤍

Ergaa kamiyyuu ergaa, ani kallattiin nan argadha.
"""

    await update.message.reply_text(welcome_message)

# ================= HANDLE MESSAGE =================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    text = update.message.text

    # ================= AUTO REPLY =================

    luxury_reply = f"""
✨ Hello {user.first_name},

Thank you for your message 🤍
I'm currently offline and out for personal business, so replies may be delayed.

📞 If urgent call:
+251934600018

⏳ I’ll respond as soon as possible.

━━━━━━━━━━━━━━━

✨ ሰላም {user.first_name},

መልእክትዎን ስላደረሱ እናመሰግናለን 🤍
አሁን በግል ስራ ላይ ስለሆንኩ ከመስመር ውጭ ነኝ።

📞 አስቸኳይ ከሆነ ይደውሉ:
+251934600018

⏳ በተቻለ ፍጥነት እመልሳለሁ።

━━━━━━━━━━━━━━━

✨ Akkam {user.first_name},

Ergaa keessaniif galatoomaa 🤍
Amma hojii dhuunfaa irratti waanan jiruuf online miti.

📞 Yoo ariifachiisaa ta’e bilbilaa:
+251934600018

⏳ Yeroon argadhetti deebii nan kenna.

🌹 Galatoomaa
"""

    # Reply to user
    await update.message.reply_text(luxury_reply)

    # ================= SEND TO ADMIN =================

    admin_message = f"""
📩 New Message

👤 Name: {user.first_name}
🆔 User ID: {user.id}
📨 Username: @{user.username}

━━━━━━━━━━━━━━━

📨 Message:
{text}
"""

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=admin_message
    )

# ================= MAIN =================

async def main():

    bot_app = Application.builder().token(TOKEN).build()

    bot_app.add_handler(
        CommandHandler("start", start)
    )

    bot_app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
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
