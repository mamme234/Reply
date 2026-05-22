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

app = Flask(__name__)

bot_app = Application.builder().token(TOKEN).build()


# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot is running with webhook!")


# ECHO MESSAGE
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        await update.message.reply_text(f"📩 {update.message.text}")


bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


# WEBHOOK ROUTE
@app.post(f"/{TOKEN}")
async def webhook():
    data = request.get_json(force=True)

    update = Update.de_json(data, bot_app.bot)

    await bot_app.process_update(update)

    return "OK", 200


async def setup():
    await bot_app.initialize()
    await bot_app.start()

    webhook_url = f"{WEBHOOK_URL}/{TOKEN}"

    await bot_app.bot.set_webhook(webhook_url)

    print(f"✅ Webhook set: {webhook_url}")


if __name__ == "__main__":
    asyncio.run(setup())

    app.run(host="0.0.0.0", port=PORT)
