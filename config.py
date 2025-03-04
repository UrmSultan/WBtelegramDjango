import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WB_API_URL = "https://suppliers-api.wildberries.ru"
WB_API_KEY = os.getenv("WB_API_KEY")

DB_NAME = "wb_bot.sqlite"
