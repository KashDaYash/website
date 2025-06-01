
import os
from pyrogram import Client, filters

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Client("uploader_bot",
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN)

@bot.on_message(filters.command("upload") & filters.reply)
async def upload_video(_, message):
    video = message.reply_to_message.video
    if not video:
        return await message.reply("Please reply to a video.")
    msg = await message.reply("Downloading...")
    file_path = await message.reply_to_message.download(file_name="static/uploads/")
    file_name = os.path.basename(file_path)
    await msg.edit(f"✅ Uploaded\n🎬 [Watch Now](https://yourapp.herokuapp.com/watch/{file_name})", disable_web_page_preview=True)

bot.run()
