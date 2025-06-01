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
    await msg.edit(f"✅ Uploaded\n🎬 [Watch Now](https://streamplayer-3a5dc841635a.herokuapp.com/watch/{file_name})", disable_web_page_preview=True)

excl = lambda cmd, prefixes=['/','.', '!'], cs=True: filters.command(cmd, prefixes, cs)
cmd = filters.command 
regex = filters.regex 
IKM =InlineKeyboardMarkup
IKB = InlineKeyboardButton 

CHAT_ID = -1002074616947
OWNER_ID = 1302298741
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

@app.on_edited_message(excl('eval'))
@app.on_message(excl('eval'))
async def eval(client, message):
    if message.from_user.id != OWNER_ID:
        return
    if len(message.command) == 1:
        return await message.reply("What You Want To Stuff")
    cmd = "".join(message.text.split(None, 1)[1:])
    if "config.py" in cmd:
        return await message.reply_text(
            "#PRIVACY_ERROR\nCan't access config.py`",
            reply_to_message_id=message.id)
    print(cmd)
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
        '''bimsi = await app.send_document(chat_id=CHAT_ID,
            document=filename,
            caption=
            f"**INPUT:**\n`cmd[0:980]`\n\n**OUTPUT:**\n`Attached Document`",
            reply_markup=keyboard)
        await message.reply(f"Your : [Result]({bimsi.link})",parse_mode=enums.ParseMode.MARKDOWN)'''
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


@app.on_callback_query(regex('^evclose$'), group=50)
async def closer(client, q):
    if q.from_user.id != q.message.reply_to_message.from_user.id:
        return
    await q.message.delete()



bot.run()
