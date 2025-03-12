from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

import database
from keyboards import main_menu_keyboard, auth_keyboard

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    user_id = message.from_user.id
    wb_token = database.get_user_token(user_id)

    if wb_token:
        await message.answer(
            "✅ Вы уже авторизованы! Выберите действие:",
            reply_markup=main_menu_keyboard()
        )
        return
    else:
        await message.answer(
            "❌ Вам нужно авторизоваться перед работой с ботом.\nНажмите кнопку ниже:",
            reply_markup=auth_keyboard()
        )
