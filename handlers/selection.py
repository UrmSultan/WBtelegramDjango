from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from handlers.storage import user_products

router = Router()

@router.callback_query(lambda call: call.data.startswith("product_"))
async def callback_product(call:CallbackQuery):
    user_id = call.from_user.id
    nm_id = call.data.removeprefix("product_")

    products = user_products.get(user_id,[])
    product = next((p for p in products if str(p["nmID"]) == nm_id), None)

    if not product:
        await call.message.answer("❌ Не могу найти этот товар в кэше. Попробуйте снова.")
        await call.answer()
        return

    sizes = product.get("sizes",[])
    if not sizes:
        await call.message.answer("❌ Для этого товара нет размеров.")
        await call.answer()
        return

    SIZE_ORDER = {
        "XXXS": 1, "XXS": 2, "XS": 3, "S": 4, "SM": 5, "M": 6, "L": 7, "XL": 8, "XXL": 9, "XXXL": 10, "4XL": 11,
        "5XL": 12
    }

    def sort_key(size):
        tech_size = size.get("techSize","NoSize")

        # print(f"DEBUG: tech_size = {tech_size}, type = {type(tech_size)}")

        if callable(tech_size):
            tech_size = tech_size()

        tech_size = str(tech_size).strip()
        try:
            return 0, float(str(tech_size))
        except ValueError:
            return 1,SIZE_ORDER.get(tech_size, 999), tech_size

    sizes_sorted = sorted(sizes, key=sort_key)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=size.get("techSize", "NoSize"),
                    callback_data=f"size_{nm_id}_{size['chrtID']}_{size['skus'][0]}_{size['techSize'].replace(' ', '-')}"
                )
            ]
            for size in sizes_sorted if size.get("skus")
        ]
    )
    await call.message.answer("Выберите размер:", reply_markup=keyboard)
    await call.answer()