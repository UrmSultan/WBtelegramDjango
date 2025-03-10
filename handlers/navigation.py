from aiogram import Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from handlers.storage import user_products, user_page

router = Router()
user_page = {}

def generate_products_keyboard(products, page: int):
    per_page = 5
    total_pages = max(1,(len(products) + per_page - 1) // per_page)
    start_idx = page * per_page
    end_idx = start_idx + per_page
    page_products = products[start_idx:end_idx]

    keyboard = [
        [InlineKeyboardButton(
            text=f"{p.get('title', 'Без названия')} / {p.get('vendorCode', 'N/A')}",
            callback_data=f"product_{p['nmID']}"
        )] for p in page_products
    ]

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅ Назад", callback_data=f"page_{page - 1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(text="➡ Вперёд", callback_data=f"page_{page + 1}"))


    if nav_buttons:
        keyboard.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@router.callback_query(lambda call: call.data.startswith("page_"))
async def page_products(call: CallbackQuery):
    user_id = call.from_user.id
    products = user_products.get(user_id,[])

    if not products:
        await call.message.answer("❌ Ошибка: список товаров пуст.")
        return

    new_page = int(call.data.split("_")[1])
    user_page[user_id] = new_page

    print(f"📦 Переключаемся на страницу {new_page}")

    keyboard = generate_products_keyboard(products, new_page)

    await call.message.edit_text(
        text=f"📦 Ваши товары (страница {new_page + 1}):",
        reply_markup=keyboard

    )
    await call.answer()