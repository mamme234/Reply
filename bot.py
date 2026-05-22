import os
import asyncio
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

if not TOKEN:
    raise ValueError("BOT_TOKEN missing")

if not WEBHOOK_URL:
    raise ValueError("WEBHOOK_URL missing")

flask_app = Flask(__name__)

telegram_app = Application.builder().token(TOKEN).build()


# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot is running!")


# ECHO
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        await update.message.reply_text(f"📩 {update.message.text}")


telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
)


# WEBHOOK
@flask_app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)

    asyncio.run(telegram_app.process_update(update))

    return "ok"


# HOME
@flask_app.route("/")
def home():
    return "Bot is alive!"


async def setup():
    await telegram_app.initialize()
    await telegram_app.start()

    webhook = f"{WEBHOOK_URL}/{TOKEN}"

    await telegram_app.bot.set_webhook(webhook)

    print(f"✅ Webhook set: {webhook}")


if __name__ == "__main__":
    asyncio.run(setup())

    flask_app.run(host="0.0.0.0", port=PORT)
