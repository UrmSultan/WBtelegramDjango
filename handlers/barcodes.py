from aiogram import Router
from aiogram.types import CallbackQuery, BufferedInputFile

from utils.barcode_generator import generate_barcode

router = Router()

@router.callback_query(lambda call: call.data.startswith("product_"))
async def handle_product(call: CallbackQuery):
    nm_id = call.data.removeprefix("product_")

    barcode_fileobj = generate_barcode(nm_id)

    barcode_bytes = barcode_fileobj.getvalue()

    file_for_telegram = BufferedInputFile(
        file=barcode_bytes
        , filename=f"{nm_id}.png")

    await call.message.answer_photo(
        photo=file_for_telegram,
        caption=f"Штрих-код для nmID {nm_id}"
    )

    await call.answer()