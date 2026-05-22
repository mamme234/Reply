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

# Your Telegram ID
ADMIN_ID = 7154361039

# Bot status
STATUS = "offline"

# ================= FLASK =================

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running successfully!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ================= FULL AUTO REPLY =================

full_text = """
🇬🇧 English:
I am currently unavailable due to private business commitments.
Kindly note that I may not respond immediately.
For urgent matters, please contact me directly at +251934600018.
Thank you for your patience and understanding.

━━━━━━━━━━━━━━━

🟡 Afaan Oromo:
Ani yeroo ammaa hojii dhuunfaa koo irratti waanan hojjetaa jiruuf argamuu hin danda’u.
Dhimmi ariifachiisaa yoo jiraate, bilbila naaf godhaa: +251934600018.
Galatoomaa obsa fi hubannoo keessaniif.

━━━━━━━━━━━━━━━

🇪🇹 Amharic:
እኔ አሁን በግል ስራ ላይ በመሆኔ ለመገኘት አልችልም።
አስቸኳይ ከሆነ ይደውሉ: +251934600018
እናመሰግናለን።
"""

# ================= SHORT ONLINE MESSAGE =================

short_text = """
🇬🇧 I'm currently online. Send your message.

🟡 Ani amma online irra jira. Ergaa keessan ergaa.

🇪🇹 አሁን መስመር ላይ ነኝ። መልእክትዎን ይላኩ።
"""

# ================= START COMMAND =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    welcome_message = """
✨ Welcome ✨

Send your message here 🤍

━━━━━━━━━━━━━━━

✨ እንኳን ደህና መጡ ✨

መልእክትዎን ይላኩ።

━━━━━━━━━━━━━━━

✨ Baga nagaan dhuftan ✨

Ergaa keessan ergaa 🤍
"""

    await update.message.reply_text(welcome_message)

# ================= ONLINE COMMAND =================

async def online(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global STATUS

    if update.effective_user.id != ADMIN_ID:
        return

    STATUS = "online"

    await update.message.reply_text("🟢 ONLINE MODE ENABLED")

# ================= OFFLINE COMMAND =================

async def offline(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global STATUS

    if update.effective_user.id != ADMIN_ID:
        return

    STATUS = "offline"

    await update.message.reply_text("🔴 OFFLINE MODE ENABLED")

# ================= MESSAGE HANDLER =================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    user = update.effective_user
    text = update.message.text or ""

    # ================= SEND MESSAGE TO ADMIN =================

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

    # ================= AUTO REPLY =================

    try:

        if STATUS == "online":
            await update.message.reply_text(short_text)

        else:
            await update.message.reply_text(full_text)

    except Exception as e:
        print("Reply Error:", e)

# ================= MAIN =================

def main():

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("online", online))
    application.add_handler(CommandHandler("offline", offline))

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("🤖 Bot started successfully...")

    application.run_polling(drop_pending_updates=True)

# ================= RUN =================

if __name__ == "__main__":

    threading.Thread(target=run_web).start()

    main()
