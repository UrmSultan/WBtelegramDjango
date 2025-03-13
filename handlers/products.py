from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


import database
from handlers.navigation import generate_products_keyboard
from keyboards import auth_keyboard
from api import get_all_products
from handlers.storage import (
    user_products,
    user_page,
    user_all_products,
    user_categories
)

router = Router()


@router.message(lambda message: message.text == "📦 Выбрать товар")
async def choose_product(message: Message):
    user_id = message.from_user.id

    wb_token = database.get_user_token(user_id)
    if not wb_token:
        await message.answer("❌ Вы не авторизованы!",reply_markup=auth_keyboard())
        return

    products = await get_all_products(wb_token)
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

    wb_token = database.get_user_token(user_id)
    if not wb_token:
        await call.message.answer("❌ Вы не авторизованы!")
        return

    all_products = user_products.get(user_id, [])
    if not all_products:
        await call.message.answer("❌ Список товаров пуст (в хранилище).")
        await call.answer()
        return


    print(f"🔍 Показываем {len(all_products)} товаров на странице")

    from collections import defaultdict
    categories_dict = defaultdict(list)
    for p in all_products:
        category=p.get("subjectName","Без категории")
        categories_dict[category].append(p)


    user_all_products[user_id] = all_products
    user_categories[user_id] = categories_dict

    keyboard_buttons = []

    for cat_name in user_categories[user_id].keys():
        cb_data = f"cat_{cat_name.replace(' ','_')}"
        keyboard_buttons.append([
            InlineKeyboardButton(text=cat_name, callback_data=cb_data)
        ])

    keyboard_buttons.append([
        InlineKeyboardButton(
            text="🔍📋 Показать весь список (полностью)",
            callback_data="show_entire_list"
        )
    ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    await call.message.edit_text(
        "Выберите категорию или показать все:",
        reply_markup=keyboard
    )
    await call.answer()

@router.callback_query(lambda call: call.data.startswith("cat_"))
async def show_category_products(call: CallbackQuery):
    user_id = call.from_user.id
    raw_cat = call.data.removeprefix("cat_")
    cat_name = raw_cat.replace('_',' ')

    categories = user_categories.get(user_id, {})
    if cat_name not in categories:
        await call.message.answer("❌ Не могу найти выбранную категорию в хранилище.")
        await call.answer()
        return

    cat_products = categories[cat_name]
    if not cat_products:
        await call.message.answer("❌ В этой категории нет товаров.")
        await call.answer()
        return

    user_products[user_id] = cat_products
    user_page[user_id] = 0
    keyboard = generate_products_keyboard(cat_products,0)
    await call.message.edit_text(
        f"Товары в категории: {cat_name}",
        reply_markup=keyboard
    )
    await call.answer()


@router.callback_query(lambda call: call.data == "show_entire_list")
async def show_entire_list(call: CallbackQuery):
    user_id = call.from_user.id

    all_products = user_products.get(user_id,[])
    if not all_products:
        await call.message.answer("❌ Список товаров пуст.")
        await call.answer()
        return

    user_products[user_id] = all_products
    user_page[user_id] = 0

    keyboard = generate_products_keyboard(all_products, 0)
    await call.message.edit_text("Полный список товаров:", reply_markup=keyboard)
    await call.answer()