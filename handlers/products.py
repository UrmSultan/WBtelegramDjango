from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

import database
from keyboards.reply import auth_keyboard
from utils.wildberries import get_wb_products

router = Router()

@router.message(lambda message: message.text == "📦 Выбрать товар")
async def choose_product(message: Message):
    user_id = message.from_user.id
    wb_token = database.get_user_token(user_id)

    if not wb_token:
        await message.answer(
            "❌ Вы не авторизованы! Нажмите '🔑 Авторизоваться'",
            reply_markup=auth_keyboard()
        )
        return

    products = await get_wb_products(wb_token)

    if not products:
        await message.answer("❌ У вас нет товаров в Wildberries.")
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=product.get("title", "Без названия"),
                callback_data=f"product_{product['nmID']}"
            )]
            for product in products[:10]
        ]
    )

    await message.answer("📦 Ваши товары:", reply_markup=keyboard)