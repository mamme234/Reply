import os
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

CHANNEL = "@KING_OF_CRY"

mode = "ai"
msg_count = 0


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
    except:
        return "AI error"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("AI", callback_data="ai"),
            InlineKeyboardButton("LUX", callback_data="lux")
        ],
        [InlineKeyboardButton("STATS", callback_data="stats")]
    ]

    await update.message.reply_text(
        "Bot ready",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global mode
    q = update.callback_query
    await q.answer()

    if q.data == "ai":
        mode = "ai"
        await q.edit_message_text("AI ON")

    elif q.data == "lux":
        mode = "lux"
        await q.edit_message_text("LUX ON")

    elif q.data == "stats":
        await q.edit_message_text(f"Messages: {msg_count}")


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global msg_count
    msg_count += 1

    text = update.message.text

    try:
        await context.bot.send_message(chat_id=CHANNEL, text=text)
    except:
        pass

    if mode == "ai":
        await update.message.reply_text(ai_reply(text))
    else:
        await update.message.reply_text("Luxury mode active")


def main():
    print("🚀 BOT STARTING...")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("BOT RUNNING")
    app.run_polling()


if __name__ == "__main__":
    main()
