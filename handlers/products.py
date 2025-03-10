from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


import database
from handlers.navigation import generate_products_keyboard
from keyboards.reply import auth_keyboard
from api.products import get_wb_products
from handlers.storage import user_products, user_page

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

    print(f"DEBUG: Получено {len(products)} товаров")

    if not products:
        await message.answer("❌ У вас нет товаров в Wildberries.")
        return

    user_products[user_id] = products

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔍 Поиск товара", callback_data="search")],
            [InlineKeyboardButton(text="🔍📋 Показать все", callback_data="show_all")]
        ]
    )

    await message.answer("📦 Ваши товары:", reply_markup=keyboard)


@router.callback_query(lambda call: call.data == "show_all")
async def show_all_products(call: CallbackQuery):
    user_id = call.from_user.id
    products = user_products.get(user_id,[])
    user_page[user_id] = 0

    if not products:
        await call.message.answer("❌ Список товаров пуст.")
        await call.answer()
        return


    print(f"🔍 Показываем {len(products)} товаров на странице {user_page[user_id]}")

    keyboard = generate_products_keyboard(products, user_page[user_id])
    print(f"DEBUG: keyboard = {keyboard}")
    await call.message.edit_text("📦 Ваши товары (страница 1):", reply_markup=keyboard)
    await call.answer()