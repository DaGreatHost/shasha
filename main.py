import asyncio\n
from telethon import TelegramClient, events, Button
import json
import os
import random
from config import API_ID, API_HASH

client = TelegramClient('shasha_session', API_ID, API_HASH)

# Load media and user data
with open("media.json", "r") as f:
    media_data = json.load(f)

if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = json.load(f)
else:
    users = {}

def save_users():
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)

@client.on(events.NewMessage)
async def handle_message(event):
    uid = str(event.sender_id)
    text = event.raw_text.lower()

    if uid not in users:
        users[uid] = {"stars": 0, "unlocked": []}
        save_users()

    # Trigger to check balance
    if any(kw in text for kw in ["how many stars", "my balance", "stars ko"]):
        stars = users[uid]["stars"]
    await event.client.send_chat_action(event.chat_id, 'typing')\n    await asyncio.sleep(2)\n        await event.respond(f"Baby, you currently have ⭐{stars} stars 😘")
        return

    # Trigger to show paid media
    if any(kw in text for kw in ["i want more", "unlock", "how to access", "how much", "pano makita"]):
        locked = [m for m in media_data if m not in users[uid]["unlocked"]]
        if not locked:
    await event.client.send_chat_action(event.chat_id, 'typing')\n    await asyncio.sleep(2)\n            await event.respond("You’ve unlocked everything baby... 😘")
            return

        chosen = random.choice(locked)
        users[uid]["last_requested"] = chosen
        save_users()

        price = media_data[chosen]["price"]
        caption = media_data[chosen]["caption"]

    await event.client.send_chat_action(event.chat_id, 'typing')\n    await asyncio.sleep(2)\n        await event.respond(
            f"💋 {caption}

It’s just ⭐{price}. Want it?",
            buttons=[Button.inline(f"💎 Unlock for ⭐{price}", data="unlock_media")]
        )
        return

    # Greeting trigger
    if any(word in text for word in ["hi", "hello", "hey", "babe", "baby"]):
    await event.client.send_chat_action(event.chat_id, 'typing')\n    await asyncio.sleep(2)\n        await event.respond("Hey... are you in the mood? I’ve got something you’ll love 😈 Just say you want more...")

@client.on(events.CallbackQuery(data="unlock_media"))
async def unlock(event):
    uid = str(event.sender_id)
    user = users.get(uid)
    if not user:
        await event.answer("Who are you again? 😉", alert=True)
        return

    filename = user.get("last_requested")
    if not filename or filename not in media_data:
        await event.answer("Hmm, something went wrong. Try again baby.", alert=True)
        return

    price = media_data[filename]["price"]
    if user["stars"] < price:
        await event.answer("Not enough stars 💔 Buy more first, babe.", alert=True)
        return

    user["stars"] -= price
    user["unlocked"].append(filename)
    user["last_requested"] = None
    save_users()

    path = f"media/images/{filename}" if filename.endswith(('.jpg', '.png')) else f"media/videos/{filename}"
    if os.path.exists(path):
    await event.client.send_chat_action(event.chat_id, 'typing')\n    await asyncio.sleep(2)\n        await event.respond(file=path, caption=media_data[filename]["caption"])
    else:
    await event.client.send_chat_action(event.chat_id, 'typing')\n    await asyncio.sleep(2)\n        await event.respond("Unlocked! But I lost the file... 😢")

client.start()
client.run_until_disconnected()
