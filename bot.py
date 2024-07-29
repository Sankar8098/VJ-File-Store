import re
import os
import logging
import asyncio
import importlib
from pathlib import Path
from pyrogram import Client, idle, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant, FloodWait
from aiohttp import web
from datetime import date, datetime
import pytz
import glob  # Import the glob module

from config import LOG_CHANNEL, ON_HEROKU, CLONE_MODE, PORT, AUTH_CHANNEL, DEF_CAP
from Script import script
from plugins.clone import restart_bots
from TechVJ.server import web_server
from TechVJ.utils.keepalive import ping_server
from TechVJ.bot.clients import initialize_clients

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

# Initialize StreamBot globally
StreamBot = Client("StreamBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def start():
    await StreamBot.start()

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

async def is_subscribed(bot, user_id, channel_ids):
    btn = []
    for channel_id in channel_ids:
        try:
            chat = await bot.get_chat(channel_id)
            invite_link = chat.invite_link or await bot.export_chat_invite_link(channel_id)
            try:
                await bot.get_chat_member(channel_id, user_id)
            except UserNotParticipant:
                btn.append([InlineKeyboardButton(f'Join {chat.title}', url=invite_link)])
            except Exception as e:
                logging.error(f"Error checking subscription status for {channel_id}: {e}")
        except Exception as e:
            logging.error(f"Error fetching chat details for {channel_id}: {e}")
    return btn

@StreamBot.on_message(filters.private)
async def on_start(client, message):
    if message.edit_date:
        return  # Ignore edited messages
    if AUTH_CHANNEL:
        try:
            btn = await is_subscribed(client, message.from_user.id, AUTH_CHANNEL)
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
            logging.error(f"Error in on_start handler: {e}")

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
        asyncio.run(start())  # Use asyncio.run to start the event loop
    except KeyboardInterrupt:
        logging.info('Service Stopped Bye 👋')
