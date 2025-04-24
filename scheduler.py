
import asyncio
import random
import os
from telethon import TelegramClient
from telethon.tl.types import InputMediaUploadedPhoto
from telethon import events
from config import API_ID, API_HASH
from seductive_lines import media_captions

client = TelegramClient('shasha_session', API_ID, API_HASH)

active_users = set()

async def send_scheduled_messages():
    await client.start()
    while True:
        if active_users:
            # Random image file
            images_path = "media/images"
            images = [f for f in os.listdir(images_path) if f.endswith(('.jpg', '.png'))]
            if images:
                chosen = random.choice(images)
                caption = random.choice(media_captions)
                for user_id in active_users:
                    try:
                        await client.send_file(user_id, f"{images_path}/{chosen}", caption=f"🔐 {caption}

Say 'unlock' if you want more 😘")
                    except Exception as e:
                        print(f"Failed to message {user_id}: {e}")
        await asyncio.sleep(1800)  # 30 minutes

@client.on(events.NewMessage)
async def track_user(event):
    active_users.add(event.sender_id)

loop = asyncio.get_event_loop()
loop.create_task(send_scheduled_messages())
client.run_until_disconnected()
