from aiogram import Router
from aiogram.filters import callback_data
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

import database
from keyboards.reply import auth_keyboard
from utils.wildberries import get_wb_products

router = Router()

user_products = {}

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

    user_products[user_id] = products

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

@router.callback_query(lambda call: call.data.startswith("product_"))
async def callback_product(call:CallbackQuery):
    user_id = call.from_user.id
    nm_id = call.data.removeprefix("product_")

    products = user_products.get(user_id,[])
    products = next((p for p in products if str(p["nmID"]) == nm_id), None)

    if not products:
        await call.message.answer("❌ Не могу найти этот товар в кэше. Попробуйте снова.")
        await call.answer()
        return

    sizes = products.get("sizes",[])
    if not sizes:
        await call.message.answer("❌ Для этого товара нет размеров.")
        await call.answer()
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=size.get("techSize", "NoSize"),
                    callback_data=f"size_{nm_id}_{size['chrtID']}_{size['skus'][0]}"
                )
            ]
            for size in sizes if size.get("skus")
        ]
    )
    await call.message.answer("Выберите размер:", reply_markup=keyboard)
    await call.answer()