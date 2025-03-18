from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import database
import aiohttp
from keyboards import main_menu_keyboard

router = Router()

class AuthState(StatesGroup):
    waiting_for_token = State()

@router.message(lambda message: message.text == "🔑 Авторизоваться")
async def auth(message: Message, state: FSMContext):
    await message.answer(
        "📝 Введите ваш Wildberries API-токен:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AuthState.waiting_for_token)


@router.message(AuthState.waiting_for_token)
async def process_wb_token(message: Message, state: FSMContext):
    user_id = message.from_user.id
    wb_token = message.text.strip()

    if not await validate_wb_token(wb_token):
        await message.answer("❌ Неверный API-токен! Попробуйте снова.")
        return

    database.save_user_token(user_id, wb_token)
    await state.clear()
    await message.answer(
        "✅ Авторизация прошла успешно! Теперь вы можете выбрать товар.",
        reply_markup=main_menu_keyboard()
    )

async def validate_wb_token(token: str) -> bool:
    url = "https://common-api.wildberries.ru/ping"
    headers = {"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            print(f"🔍 Проверка токена: {token} → {response.status}")
            return response.status == 200

@router.message(lambda message: message.text == "🚪 Выйти из аккаунта")
async def logout(message: Message):
    user_id = message.from_user.id

    database.delete_user_token(user_id)
    await message.answer(
        "✅ Вы успешно вышли из аккаунта.\nТеперь, если понадобится, авторизуйтесь заново:",
        reply_markup=main_menu_keyboard()
    )