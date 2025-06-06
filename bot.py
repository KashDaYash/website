from pyrogram import Client, filters, idle, enums
import os
import re
import subprocess
import sys
import traceback
from inspect import getfullargspec
from io import StringIO, BytesIO 
from time import time
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery 
import io
import aiohttp 


API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = -1002074616947
OWNER_ID = 1302298741

bot = Client("uploader_bot",
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN)

@bot.on_message(filters.command("upload") & filters.reply & filters.user(OWNER_ID))
async def upload_video(_, message):
    video = message.reply_to_message.video
    if not video:
        return await message.reply("Please reply to a video.")
    msg = await message.reply("Downloading...")

    file_name = f"{video.file_unique_id}.mp4"
    save_path = os.path.join("static", "uploads", file_name)
    await message.reply_to_message.download(file_name=save_path)

    await msg.edit(
        f"✅ Uploaded\n🎬 [Watch Now](https://streamplayer-3a5dc841635a.herokuapp.com/watch/{file_name})",
        disable_web_page_preview=True
    )
excl = lambda cmd, prefixes=['/','.', '!'], cs=True: filters.command(cmd, prefixes, cs)
cmd = filters.command 
regex = filters.regex 
IKM =InlineKeyboardMarkup
IKB = InlineKeyboardButton 

async def aexec_(code, message, client):
    m = event = message
    p = lambda x: print(x)

    exec_scope = {}
    exec(
        "async def __aexec(m, event, message, client, p):\n"
        + "\n".join(f"    {line}" for line in code.split("\n")),
        exec_scope,
    )

    return await exec_scope["__aexec"](m, event, message, client, p)

@bot.on_edited_message(excl('eval'))
@bot.on_message(excl('eval'))
async def eval(client, message):
    if message.from_user.id != OWNER_ID:
        return
    if len(message.command) == 1:
        return await message.reply("What You Want To Stuff")
    cmd = "".join(message.text.split(None, 1)[1:])
    if not cmd:
        return await message.reply_text("What should I run?")
    eva = await message.reply_text("Running...")
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec_(cmd, message, client)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = (
        f"⥤ ᴇᴠᴀʟ : \n<pre>{cmd}</pre> \n\n⥤ ʀᴇsᴜʟᴛ : \n<pre>{evaluation}</pre>"
    )
    if len(final_output) > 4096:
        filename = "result.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(evaluation.strip()))
        keyboard = IKM([[
            IKB(
                text="🗑",
                callback_data="evclose",
            )
        ]])
        await message.reply_document(document=filename, caption=f"**INPUT:**\n`cmd[0:980]`\n\n**OUTPUT:**\n`Attached Document`",reply_markup=keyboard,parse_mode=enums.ParseMode.MARKDOWN)
        await eva.delete()
        os.remove(filename)
    else:
        keyboard = IKM([[
            IKB(
                text="🗑",
                callback_data="evclose",
            )
        ]])
        await eva.edit_text(text=final_output, reply_markup=keyboard)


@bot.on_callback_query(regex('^evclose$'), group=50)
async def closer(client, q):
    if q.from_user.id != q.message.reply_to_message.from_user.id:
        return
    await q.message.delete()

async def get_yaara_data(endpoint: str):
    url = f"https://yaaraapi-db1b9186ba12.herokuapp.com/{endpoint}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get(endpoint)
            else:
                return "tujh se hoga?"

@bot.on_message(filters.command("truth"))
async def truth_command(_, message):
    truth = await get_yaara_data("truth")
    await message.reply_text(f"🧠 Truth:\n{truth}")

# /dare command
@bot.on_message(filters.command("dare"))
async def dare_command(_, message):
    dare = await get_yaara_data("dare")
    await message.reply_text(f"🎯 Dare:\n{dare}")

bot.run()
