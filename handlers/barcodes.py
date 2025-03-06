from aiogram import Router
from aiogram.types import CallbackQuery

from utils.barcode_generator import generate_ean13


router = Router()

@router.callback_query(lambda call: call.data.startswith("size_"))
async def handle_product(call: CallbackQuery):

    parts = call.data.split("_") # ["size", nmID, chrtID, sku]
    if len(parts) < 4:
        await call.message.answer("❌ Неверный формат callback_data.")
        await call.answer()
        return

    nm_id = parts[1]
    chrt_id = parts[2]
    sku_13 = parts[3]

    if len(sku_13) != 13 or not sku_13.isdigit():
        await call.message.answer("❌ SKU не является 13-значным числом!")
        await call.answer()
        return

    barcode_png = generate_ean13(sku_13)

    await call.message.answer_photo(
        photo=barcode_png,
        caption=f"EAN-13 для SKU {sku_13}\n Товар nmID{nm_id}\n chrtID {chrt_id}",
    )

    await call.answer()