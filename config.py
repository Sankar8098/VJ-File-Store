import re
import os
from Script import script

id_pattern = re.compile(r'^.\d+$')

def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default
      
# Bot Information
API_ID = int(os.environ.get("API_ID", "23990433"))
API_HASH = os.environ.get("API_HASH", "e6c4b6ee1933711bc4da9d7d17e1eb20")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7450625675:AAEWPP-I4rQmM4Qr9HtlOkH9G5-ielfV1D0")

PICS = os.environ.get('PICS', 'https://graph.org/file/ce1723991756e48c35aa1.jpg').split()  # Bot Start Picture
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMINS', '5821871362').split()]
AUTH_CHANNEL = [int(ch) if id_pattern.search(ch) else ch for ch in os.environ.get('AUTH_CHANNEL', '-1001864683653').split()]  # give channel id with separate space. Ex : ('-10073828 -102782829 -1007282828')
BOT_USERNAME = os.environ.get("BOT_USERNAME", "File_store_streaming_bot")  # without @
PORT = int(os.environ.get("PORT", "8080"))

# Clone Info:
CLONE_MODE = is_enabled(os.environ.get('CLONE_MODE', "True"), True)  # Set True or False

# If Clone Mode Is True Then Fill All Required Variable, If False Then Don't Fill.
CLONE_DB_URI = os.environ.get("CLONE_DB_URI", "mongodb+srv://clonefilestorebot:1234@clonefilestorebot.xuymndi.mongodb.net/?retryWrites=true&w=majority&appName=clonefilestorebot")
CDB_NAME = os.environ.get("CDB_NAME", "clonetechvj")

# Database Information
DB_URI = os.environ.get("DB_URI", "mongodb+srv://Filestorebot:1234@filestorebot.egd2ux0.mongodb.net/?retryWrites=true&w=majority&appName=Filestorebot")
DB_NAME = os.environ.get("DB_NAME", "techvj")

# Auto Delete Information
AUTO_DELETE_MODE = is_enabled(os.environ.get('AUTO_DELETE_MODE', "False"), False)  # Set True or False

# If Auto Delete Mode Is True Then Fill All Required Variable, If False Then Don't Fill.
AUTO_DELETE = int(os.environ.get("AUTO_DELETE", "30"))  # Time in Minutes
AUTO_DELETE_TIME = int(os.environ.get("AUTO_DELETE_TIME", "1800"))  # Time in Seconds

# Channel Information
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001870015374"))
DEF_CAP = os.environ.get(
    "DEF_CAP",
    "<b><a href='telegram.me/SK_MoviesOffl'>{file_name} Telegram : @SK_MoviesOffl\n\nForward the file before Downloading.</a></b>"
)

# File Caption Information
CUSTOM_FILE_CAPTION = os.environ.get("CUSTOM_FILE_CAPTION", f"{script.CAPTION}")
BATCH_FILE_CAPTION = os.environ.get("BATCH_FILE_CAPTION", CUSTOM_FILE_CAPTION)

# Enable - True or Disable - False
PUBLIC_FILE_STORE = is_enabled(os.environ.get('PUBLIC_FILE_STORE', "True"), True)

# Verify Info:
VERIFY_MODE = is_enabled(os.environ.get('VERIFY_MODE', "False"), False)  # Set True or False

# If Verify Mode Is True Then Fill All Required Variable, If False Then Don't Fill.
SHORTLINK_API = os.environ.get("SHORTLINK_API", "")  # shortlink api
SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "")  # shortlink domain without https://
VERIFY_TUTORIAL = os.environ.get("VERIFY_TUTORIAL", "")  # how to open link 

# Website Info:
WEBSITE_URL_MODE = is_enabled(os.environ.get('WEBSITE_URL_MODE', "False"), False)  # Set True or False

# If Website Url Mode Is True Then Fill All Required Variable, If False Then Don't Fill.
WEBSITE_URL = os.environ.get("WEBSITE_URL", "")  # For More Information Check Video On Yt - @Tech_VJ

# File Stream Config
STREAM_MODE = is_enabled(os.environ.get('STREAM_MODE', "True"), True)  # Set True or False

# If Stream Mode Is True Then Fill All Required Variable, If False Then Don't Fill.
MULTI_CLIENT = False
SLEEP_THRESHOLD = int(os.environ.get('SLEEP_THRESHOLD', '60'))
PING_INTERVAL = int(os.environ.get("PING_INTERVAL", "1200"))  # 20 minutes

ON_HEROKU = 'DYNO' in os.environ
URL = os.environ.get("URL", "https://file-store-bot-streaming-working.onrender.com/")

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
