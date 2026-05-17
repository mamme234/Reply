import os
import logging
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update, context):
    await update.message.reply_text("🚀 Ra Jahn Bot is Active!")

def main():
    # Check if TOKEN exists to avoid the crash you saw
    if not TOKEN:
        print("❌ ERROR: No TOKEN found in Environment Variables!")
        return

    print("🚀 BOT STARTING...")
    
    # Create the app
    app = Application.builder().token(TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))

    # Start the Bot
    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
