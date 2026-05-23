from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = 39259168
api_hash = "75ce72b0f39f07f1de897cce227c83c8"

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print(client.session.save())
