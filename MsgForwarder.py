from telethon import types
from telethon.tl.functions.messages import EditMessageRequest

import re
from telethon import TelegramClient, events
from decouple import config
import logging
from telethon.sessions import StringSession

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

# Basics
APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
SESSION = config("SESSION")
FROM_ = config("FROM_CHANNEL")
TO_ = config("TO_CHANNEL")
REPLACEUSERNAMW = config("REPLACEUSERNAME")

FROM = [int(i) for i in FROM_.split()]
TO = [int(i) for i in TO_.split()]

try:
    Client = TelegramClient(StringSession(SESSION), APP_ID, API_HASH)
    Client.start()
except Exception as ap:
    print(f"ERROR - {ap}")
    exit(1)






@client.on(events.NewMessage(outgoing=False))
async def my_event_handler(event):
    if event.chat_id in FROM:
        clipboard = str(event.raw_text)
        replaceList = []
        for item in event.get_entities_text():
            if type(item[0]) == types.MessageEntityMention or type(item[0]) == types.MessageEntityTextUrl or type(item[0]) == types.MessageEntityUrl:
                replaceList.append(item[1])
        for i in replaceList:
            if "@" in i or "t.me" in i:
                clipboard = clipboard.replace(i, REPLACEUSERNAME)
        for channel in TO:
            await client.send_message(channel, clipboard)

print("Bot has started.")
Client.run_until_disconnected()

