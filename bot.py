import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

import config
from api.session import close_session
from handlers import all_routers

# Enable logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher
bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=MemoryStorage())

# Register handlers
for router in all_routers:
    dp.include_router(router)

async def main():
    """Start polling for Telegram bot."""
    logging.info("Starting bot...")
    try:
        await dp.start_polling(bot)
    finally:
        await close_session()


if __name__ == "__main__":
    asyncio.run(main())