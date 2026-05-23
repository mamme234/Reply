import os
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")

client = TelegramClient(
    "personal_session",
    API_ID,
    API_HASH
)

AUTO_REPLY = """
🇬🇧 English:
I am currently unavailable due to private business commitments.
Kindly note that I may not respond immediately.
For urgent matters:
Call me: +251934600018

━━━━━━━━━━━━━━━

🟡 Afaan Oromo:
Ani yeroo ammaa hojii dhuunfaa koo irratti waanan hojjetaa jiruuf argamuu hin danda’u.
Dhimmi ariifachiisaa yoo jiraate:
Call me: +251934600018

━━━━━━━━━━━━━━━

🇪🇹 Amharic:
እኔ አሁን በግል ስራ ላይ በመሆኔ ለመገኘት አልችልም።
አስቸኳይ ከሆነ:
Call me: +251934600018
"""

# store users already replied to recently
recent_users = set()

@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):

    # only private chats
    if not event.is_private:
        return

    sender = await event.get_sender()

    # ignore bots
    if sender.bot:
        return

    user_id = sender.id

    # avoid spam replies
    if user_id in recent_users:
        return

    recent_users.add(user_id)

    try:
        await event.reply(AUTO_REPLY)
        print(f"Auto replied to {user_id}")

    except Exception as e:
        print(e)

print("Userbot running...")

client.start(phone=PHONE_NUMBER)
client.run_until_disconnected()
