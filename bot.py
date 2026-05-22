import os
import asyncio
import threading
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
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

# Save user languages
user_languages = {}

# ================= FLASK =================

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running successfully!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ================= LANGUAGES =================

texts = {

    "eng": {
        "selected": "Language set to English 🇬🇧",

        "offline": """
✨ Hello {name},

Thank you for your message 🤍

I'm currently offline and out for personal business, so replies may be delayed.

📞 If your message is urgent, please call:
+251934600018

⏳ I’ll respond as soon as I'm available.

Thank you for your patience 🌹
"""
    },

    "amh": {
        "selected": "ቋንቋው ወደ አማርኛ ተቀይሯል 🇪🇹",

        "offline": """
✨ ሰላም {name},

መልእክትዎን ስላደረሱ እናመሰግናለን 🤍

አሁን በግል ስራ ላይ ስለሆንኩ ከመስመር ውጭ ነኝ፣ ስለዚህ ምላሽ ሊዘገይ ይችላል።

📞 አስቸኳይ ከሆነ ይደውሉ:
+251934600018

⏳ በተቻለ ፍጥነት እመልሳለሁ።

ለትዕግስትዎ እናመሰግናለን 🌹
"""
    },

    "oro": {
        "selected": "Afaan Oromoo filatameera 🌍",

        "offline": """
✨ Akkam {name},

Ergaa keessaniif galatoomaa 🤍

Amma hojii dhuunfaa irratti waanan jiruuf online miti, deebiin isaanii yeroo fudhachuu danda’a.

📞 Yoo dhimichi ariifachiisaa ta’e bilbilaa:
+251934600018

⏳ Yeroon argadhetti deebii isiniif nan kenna.

Galatoomaa 🌹
"""
    }
}

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["English 🇬🇧"],
        ["አማርኛ 🇪🇹"],
        ["Afaan Oromo 🌍"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "Choose language / ቋንቋ ይምረጡ / Afaan filadhaa 👇",
        reply_markup=reply_markup
    )

# ================= HANDLE MESSAGE =================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    text = update.message.text

    # ================= LANGUAGE SELECTION =================

    if text == "English 🇬🇧":
        user_languages[user.id] = "eng"

        await update.message.reply_text(
            texts["eng"]["selected"]
        )
        return

    elif text == "አማርኛ 🇪🇹":
        user_languages[user.id] = "amh"

        await update.message.reply_text(
            texts["amh"]["selected"]
        )
        return

    elif text == "Afaan Oromo 🌍":
        user_languages[user.id] = "oro"

        await update.message.reply_text(
            texts["oro"]["selected"]
        )
        return

    # ================= GET USER LANGUAGE =================

    lang = user_languages.get(user.id, "eng")

    # ================= AUTO REPLY =================

    reply = texts[lang]["offline"].format(
        name=user.first_name
    )

    await update.message.reply_text(reply)

    # ================= SEND TO ADMIN =================

    admin_message = f"""
📩 New Message

👤 Name: {user.first_name}
🆔 User ID: {user.id}
🌍 Language: {lang}

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
