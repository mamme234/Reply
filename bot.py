import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot is online and working!")


# echo messages
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"📩 You said: {text}")


def main():
    if not TOKEN:
        print("❌ BOT_TOKEN missing in .env")
        return

    print("🚀 BOT STARTING...")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("✅ BOT RUNNING SUCCESSFULLY")

    app.run_polling()


if __name__ == "__main__":
    main()
