from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio

# 💾 Your Bot Credentials
API_ID = 24509589
API_HASH = "717cf21d94c4934bcbe1eaa1ad86ae75"
BOT_TOKEN = "7796568404:AAF2gRAROH7es6Mz9S8UJ-d6UZvlVC-SS5Q"

# 📌 Your Chat IDs
BACKUP_CHANNEL_ID = -1002684354063
STARTUP_NOTIFY_CHAT_ID = -1002696911386  # Group jisme bot start message jaayega

# 📦 Bot Init
app = Client("GroupMediaBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ✅ On Bot Startup
@app.on_client_ready()
async def on_startup(client: Client):
    try:
        await client.send_message(STARTUP_NOTIFY_CHAT_ID, "🤖 Bot is now online and ready to work!")
        print("✅ Startup message sent.")
    except Exception as e:
        print(f"❌ Error sending startup message: {e}")

# ✅ /msgc - Count total messages in group
@app.on_message(filters.command("msgc") & filters.group)
async def count_messages(client, message: Message):
    count = 0
    async for _ in client.get_chat_history(message.chat.id):
        count += 1
    await message.reply_text(f"📊 Total Messages in Group: {count}")

# ✅ /ancpy - Copy media to backup channel & delete from group
@app.on_message(filters.command("ancpy") & filters.group)
async def copy_and_delete_media(client, message: Message):
    copied = 0
    deleted = 0

    await message.reply_text("⏳ Starting media backup...")

    async for msg in client.get_chat_history(message.chat.id):
        if msg.media:
            try:
                await msg.copy(BACKUP_CHANNEL_ID)
                copied += 1
                await asyncio.sleep(0.5)
                await client.delete_messages(message.chat.id, msg.message_id)
                deleted += 1
            except Exception as e:
                print(f"Error: {e}")
                continue

    await message.reply_text(f"✅ Media copied: {copied}\n🗑️ Media deleted: {deleted}")

# ✅ Greet user on any normal message
@app.on_message(filters.group & ~filters.service & ~filters.command(["msgc", "ancpy"]))
async def greet_user(client, message: Message):
    user = message.from_user
    if user:
        name = user.first_name or "user"
        await message.reply_text(f"Hello, {name} 👋")

# 🚀 Run the bot
app.run()
