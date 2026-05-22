import os
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
ADMIN_ID = 7154361039

# 🟢 / 🔴 STATUS
STATUS = "offline"

# ================= FLASK =================

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running successfully!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ================= LUXURY MESSAGE (3 LANG + CALL ME) =================

full_text = """
✨ ꧁ɪ ᴀᴍ Tᕼᗴ KIᑎᘜ꧂ ✨

🇬🇧 English:
I am currently unavailable due to private business commitments.
Kindly note that I may not respond immediately.
For urgent matters, Call me: +251934600018
Thank you for your patience and understanding.

━━━━━━━━━━━━━━━

🇪🇹 Amharic:
እኔ አሁን በግል ስራ ላይ በመሆኔ ለመገኘት አልችልም።
አስቸኳይ ከሆነ ይደውሉ: +251934600018
እናመሰግናለን።

━━━━━━━━━━━━━━━

🟡 Afaan Oromo:
Ani yeroo ammaa hojii dhuunfaa koo irratti waanan hojjetaa jiruuf argamuu hin danda’u.
Dhimmi ariifachiisaa yoo jiraate, Call me: +251934600018
Galatoomaa obsa fi hubannoo keessaniif.
"""

online_text = """
🟢 ꧁ɪ ᴀᴍ Tᕼᗴ KIᑎᘜ꧂

I’m currently ONLINE.
Send your message 🤍
"""

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    welcome = """
✨ Welcome ꧁ɪ ᴀᴍ Tᕼᗴ KIᑎᘜ꧂ ✨

Send me a message 🤍
I will reply based on my status.

━━━━━━━━━━━━━━━

✨ እንኳን ደህና መጡ ✨
"""

    await update.message.reply_text(welcome)

# ================= ADMIN CONTROL =================

async def go_online(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global STATUS

    if update.effective_user.id != ADMIN_ID:
        return

    STATUS = "online"
    await update.message.reply_text("🟢 STATUS: ONLINE")

async def go_offline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global STATUS

    if update.effective_user.id != ADMIN_ID:
        return

    STATUS = "offline"
    await update.message.reply_text("🔴 STATUS: OFFLINE")

# ================= MESSAGE HANDLER =================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    text = update.message.text if update.message.text else ""

    # 👤 SEND TO YOUR PERSONAL TELEGRAM INBOX
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"""
📩 NEW MESSAGE

👤 Name: {user.first_name}
🆔 ID: {user.id}
📨 Username: @{user.username}

💬 Message:
{text}
"""
    )

    # ================= ONLINE MODE =================
    if STATUS == "online":
        await update.message.reply_text(online_text)
        return

    # ================= OFFLINE MODE =================
    await update.message.reply_text(full_text)

# ================= BOT CORE =================

def main():

    bot_app = Application.builder().token(TOKEN).build()

    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("online", go_online))
    bot_app.add_handler(CommandHandler("offline", go_offline))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")

    bot_app.run_polling()

# ================= RUN SERVER =================

if __name__ == "__main__":

    threading.Thread(target=run_web).start()
    main()
