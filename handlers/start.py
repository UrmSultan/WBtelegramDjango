from aiogram import Router
from aiogram.types import Message

import database
from keyboards import main_menu_keyboard, auth_keyboard

router = Router()

@router.message()
async def start_handler(message: Message):
    """ بِسۡمِ ٱللَّهِ ٱلرَّحۡمَـٰنِ ٱلرَّحِيمِ"""
    user_id = message.from_user.id
    wb_token = database.get_user_token(user_id)

    welcome_text = (
        "👋 Здравствуйте! Я бот для работы с Wildberries.\n"
        "Я помогу вам управлять товарами, печатать штрих-коды и многое другое! 🚀\n"
    )

    if wb_token:
        await message.answer(
            f"{welcome_text}\n✅ Вы уже авторизованы! Выберите действие:",
            reply_markup=main_menu_keyboard()
        )
        return
    else:
        await message.answer(
            f"{welcome_text}\n❌ Вам нужно авторизоваться перед работой с ботом.\nНажмите кнопку ниже:",
            reply_markup=auth_keyboard()
        )
