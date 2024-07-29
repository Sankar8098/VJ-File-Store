import sys
import glob
import importlib
from pathlib import Path
from pyrogram import Client, idle, __version__
from pyrogram.raw.all import layer
import logging
import logging.config
from typing import Union, Optional, AsyncGenerator
from aiohttp import web
from datetime import date, datetime
import pytz
import asyncio
import re

from config import LOG_CHANNEL, ON_HEROKU, CLONE_MODE, PORT, AUTH_CHANNEL, DEF_CAP
from Script import script
from plugins.clone import restart_bots
from TechVJ.server import web_server
from TechVJ.bot import StreamBot
from TechVJ.utils.keepalive import ping_server
from TechVJ.bot.clients import initialize_clients
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant, FloodWait

# Logging configuration
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

# Define the plugins path
ppath = "plugins/*.py"
files = glob.glob(ppath)

StreamBot.start()
loop = asyncio.get_event_loop()

async def start():
    print('\n')
    print('Initializing Tech VJ Bot')
    bot_info = await StreamBot.get_me()
    StreamBot.username = bot_info.username
    await initialize_clients()
    
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"plugins/{plugin_name}.py")
            import_path = "plugins.{}".format(plugin_name)
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules["plugins." + plugin_name] = load
            print("Tech VJ Imported => " + plugin_name)

    if ON_HEROKU:
        asyncio.create_task(ping_server())

    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    time = now.strftime("%H:%M:%S %p")
    app = web.AppRunner(await web_server())
    await StreamBot.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))
    await app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, PORT).start()

    if CLONE_MODE:
        await restart_bots()
        
    print("Bot Started Powered By @TN_Bots")
    await idle()

async def is_subscribed(bot, query, channel):
    btn = []
    for id in channel:
        chat = await bot.get_chat(int(id))
        try:
            await bot.get_chat_member(id, query.from_user.id)
        except UserNotParticipant:
            btn.append([InlineKeyboardButton(f'Join {chat.title}', url=chat.invite_link)])
        except Exception as e:
            pass
    return btn

@StreamBot.on_message()
async def on_start(client, message):
    if AUTH_CHANNEL:
        try:
            btn = await is_subscribed(client, message, AUTH_CHANNEL)
            if btn:
                username = (await client.get_me()).username
                if len(message.command) > 1 and message.command[1]:
                    btn.append([InlineKeyboardButton("♻️ Try Again ♻️", url=f"https://t.me/{username}?start={message.command[1]}")])
                else:
                    btn.append([InlineKeyboardButton("♻️ Try Again ♻️", url=f"https://t.me/{username}?start=true")])
                await message.reply_text(
                    text=f"<b>👋 Hello {message.from_user.mention},\n\nPlease join the channel then click on try again button. 😇</b>", 
                    reply_markup=InlineKeyboardMarkup(btn)
                )
                return
        except Exception as e:
            print(e)

@StreamBot.on_message(filters.channel)
async def auto_edit_caption(bot, message):
    chnl_id = message.chat.id
    if message.media:
        for file_type in ("video", "audio", "document", "voice"):
            obj = getattr(message, file_type, None)
            if obj and hasattr(obj, "file_name"):
                file_name = obj.file_name
                file_caption = message.caption or ""
                file_name = re.sub(r"@\w+\s*", "", file_name).replace("_", " ").replace(".", " ")
                cap_dets = await chnl_ids.find_one({"chnl_id": chnl_id})
                try:
                    if cap_dets:
                        cap = cap_dets["caption"]
                        replaced_caption = cap.format(file_name=file_name, file_caption=file_caption)
                        await message.edit(replaced_caption)
                    else:
                        replaced_caption = DEF_CAP.format(file_name=file_name, file_caption=file_caption)
                        await message.edit(replaced_caption)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    continue
    return

if __name__ == '__main__':
    try:
        loop.run_until_complete(start())
    except KeyboardInterrupt:
        logging.info('Service Stopped Bye 👋')
