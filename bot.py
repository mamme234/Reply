import os
from dotenv import load_dotenv
from flask import Flask, request

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 10000))

app = Flask(__name__)

# Telegram bot application
bot_app = Application.builder().token(TOKEN).build()


# ---------------- HANDLERS ---------------- #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Webhook Bot is running!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        await update.message.reply_text(f"📩 {update.message.text}")


bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


# ---------------- WEBHOOK ROUTE ---------------- #

@app.post("/")
async def webhook():
    data = request.get_json(force=True)

    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)

    return "OK"


# ---------------- SET WEBHOOK ON START ---------------- #

async def on_startup():
    if WEBHOOK_URL:
        await bot_app.bot.set_webhook(url=WEBHOOK_URL)
        print(f"✅ Webhook set to {WEBHOOK_URL}")


# ---------------- RUN SERVER ---------------- #

if __name__ == "__main__":
    import asyncio

    async def main():
        await on_startup()
        app.run(host="0.0.0.0", port=PORT)

    asyncio.run(main())
