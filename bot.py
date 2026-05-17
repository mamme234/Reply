import os
import time
import requests
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OWNER_ID = 7154361039
CHANNEL = "@KING_OF_CRY"

msg_count = 0
mode = "ai"

# ───────── AI FUNCTION ─────────
def ai_reply(text):
    try:
        r = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are a Telegram assistant."},
                    {"role": "user", "content": text}
                ]
            },
            timeout=20
        )

        return r.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return "⚡ AI error"

# ───────── START ─────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🤖 AI MODE", callback_data="ai"),
            InlineKeyboardButton("💼 LUXURY", callback_data="luxury")
        ],
        [InlineKeyboardButton("📊 STATS", callback_data="stats")]
    ]

    await update.message.reply_text(
        "👑 Bot Panel Ready",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ───────── BUTTONS ─────────
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global mode

    query = update.callback_query
    await query.answer()

    if query.data == "ai":
        mode = "ai"
        await query.edit_message_text("🤖 AI mode ON")

    elif query.data == "luxury":
        mode = "luxury"
        await query.edit_message_text("💼 Luxury mode ON")

    elif query.data == "stats":
        await query.edit_message_text(f"📊 Active messages bot received")

# ───────── MESSAGE HANDLER ─────────
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global msg_count, mode

    msg_count += 1
    text = update.message.text

    # forward to channel
    try:
        await context.bot.send_message(chat_id=CHANNEL, text=f"📩 {text}")
    except:
        pass

    if mode == "ai":
        reply = ai_reply(text)
        await update.message.reply_text(reply)
    else:
        await update.message.reply_text(
            "👑 Luxury mode active.\nContact admin for access."
        )

# ───────── MAIN ─────────
def main():
    print("🚀 BOT STARTING...")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("🚀 BOT RUNNING...")
    app.run_polling()

if __name__ == "__main__":
    main()
