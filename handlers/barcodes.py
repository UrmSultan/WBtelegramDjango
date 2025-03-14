from aiogram import Router
from aiogram.types import CallbackQuery

import database
from api import get_supplier_name
from handlers.storage import user_products
from utils import generate_ean13_with_info
from utils import parse_characteristic

router = Router()

@router.callback_query(lambda call: call.data.startswith("size_"))
async def callback_size_barcode(call: CallbackQuery):
    parts = call.data.split("_") # ["size", nmID, chrtID, sku]
    if len(parts) < 4:
        await call.message.answer("❌ Неверный формат callback_data.")
        await call.answer()
        return

    user_id = call.from_user.id
    nm_id = parts[1]
    sku_13 = parts[3]
    size_label = parts[4]

    # Get product from cache
    products = user_products.get(user_id, [])
    product = next((p for p in products if str(p["nmID"]) == nm_id), None)
    if not product:
        await call.message.answer("❌ Не могу найти товар в кэше. Попробуйте снова.")
        await call.answer()
        return

    # Get data from product
    title = product.get("title", "Без названия")
    brand = product.get("brand")
    color = parse_characteristic(product, "Цвет")
    material = parse_characteristic(product, "материал верха")

    # gender = parse_characteristic(product, "Пол")
    # vendor_code = product.get("vendorCode", "N/A")

    # Request sole proprietor(ИП)
    user_token = database.get_user_token(user_id)
    supplier_name = await get_supplier_name(user_token)

    # Generate img with info
    barcode_image = generate_ean13_with_info(
        sku_13=sku_13,
        title=title,
        brand=brand,
        color=color,
        material=material,
        supplier_name=supplier_name,
        size_label=size_label
    )

    # Send image to user
    await call.message.answer_photo(
        photo=barcode_image
    )

    await call.answer()