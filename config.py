import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WB_API_KEY = os.getenv("WB_API_KEY")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
DB_NAME = os.getenv("DB_NAME")
