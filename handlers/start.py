from aiogram import Router
from aiogram.types import Message

import database
from keyboards import main_menu_keyboard, auth_keyboard

router = Router()

@router.message(lambda message: message.text not in ["ℹ️ Инструкция", "/help"])
async def start_handler(message: Message):
    """ بِسۡمِ ٱللَّهِ ٱلرَّحۡمَـٰنِ ٱلرَّحِيمِ"""
    user_id = message.from_user.id
    wb_token = database.get_user_token(user_id)
    welcome_text = (
        "👋 Привет! Я бот для работы с Wildberries.\n\n"
        "Чтобы я мог управлять вашими товарами, мне нужен токен Wildberries Content API.\n"
        "Вы можете сгенерировать (или найти) его в вашем личном кабинете WB.\n\n"
        "❓ Как получить токен:\n"
        "1) Зайдите в личный кабинет на [seller.wildberries.ru].\n"
        "2) Откройте раздел «Настройки» → «Доступ к API».\n"
        "3) Скопируйте (или сгенерируйте новый) **Content API key**.\n\n"
        "Затем отправьте этот ключ мне, и я смогу:\n"
        "• Показывать ваши товары;\n"
        "• Помогать с печатью штрих-кодов;\n"
        "• И многое другое!\n"
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
