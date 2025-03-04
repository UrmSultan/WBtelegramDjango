import logging
import asyncio
import config
import database
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardRemove


# Enable logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Start command handler
@dp.message(CommandStart())
async def start_handler(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔑 Авторизоваться"), KeyboardButton(text="ℹ️ Помощь")]
        ],
        resize_keyboard=True
    )

    await message.answer("👋 Привет! Я помогу тебе создать штрих-коды для товаров WB.\nВыбери действие ниже:", reply_markup=keyboard)

@dp.message(lambda message:message.text == "🔑 Авторизоваться")
async def request_wb_token(message: Message):
    await message.answer("📝 Введите ваш Wildberries API-токен:", reply_markup=ReplyKeyboardRemove())

# Handle user input (API token)
@dp.message()
async def process_wb_token(message: Message):
    user_id = message.from_user.id
    wb_token = message.text.strip()

    # Validate token
    if not await validate_wb_token(wb_token):
        await message.answer("❌ Неверный API-токен! Попробуйте снова.")
        return

    # Save token in database
    database.save_user_token(user_id, wb_token)
    await message.answer("✅ Авторизация прошла успешно! Теперь вы можете выбрать товар.", reply_markup=start_keyboard())

async def validate_wb_token(token: str) -> bool:
    url="https://common-api.wildberries.ru/ping"
    headers = {"Authorization": token
               }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return response.status == 200

def start_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📦 Выбрать товар"), KeyboardButton(text="ℹ️ Помощь")]],
        resize_keyboard=True
    )

async def main():
    logging.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())