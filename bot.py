import os
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

STATUS = "offline"

# ================= FLASK =================

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running successfully!"

# ================= LUXURY MESSAGE =================

full_text = """
✨ ꧁ɪ ᴀᴍ Tᕼᗴ KIᑎᘜ꧂ ✨

🇬🇧 English:
I am currently unavailable due to private business commitments.
Kindly note that I may not respond immediately.
For urgent matters, Call me: +251934600018

━━━━━━━━━━━━━━━

🇪🇹 Amharic:
እኔ አሁን በግል ስራ ላይ ነኝ።
አስቸኳይ ከሆነ ይደውሉ: +251934600018

━━━━━━━━━━━━━━━

🟡 Afaan Oromo:
Ani hojii dhuunfaa irratti jira.
Call me: +251934600018
"""

online_text = "🟢 I’m online now. Send your message 🤍"

# ================= HANDLERS =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✨ Welcome! Send me a message 🤍")

async def go_online(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global STATUS
    if update.effective_user.id == ADMIN_ID:
        STATUS = "online"
        await update.message.reply_text("🟢 ONLINE MODE")

async def go_offline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global STATUS
    if update.effective_user.id == ADMIN_ID:
        STATUS = "offline"
        await update.message.reply_text("🔴 OFFLINE MODE")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    text = update.message.text

    # 👤 send to admin inbox
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"""
📩 NEW MESSAGE

👤 {user.first_name}
🆔 {user.id}

💬 {text}
"""
    )

    # 🤖 reply logic
    if STATUS == "online":
        await update.message.reply_text(online_text)
    else:
        await update.message.reply_text(full_text)

# ================= FLASK THREAD =================

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ================= MAIN =================

def main():

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("online", go_online))
    application.add_handler(CommandHandler("offline", go_offline))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot started successfully...")

    # ✅ SAFE FOR RENDER
    application.run_polling(drop_pending_updates=True)

# ================= RUN =================

if __name__ == "__main__":

    import threading
    threading.Thread(target=run_flask).start()

    main()
