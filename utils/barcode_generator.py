import io
import barcode
from aiogram.types import BufferedInputFile
from barcode.writer import ImageWriter

def generate_ean13(sku_13: str) -> BufferedInputFile:
    buffer = io.BytesIO()
    ean13 = barcode.get_barcode_class("ean13")(sku_13, writer=ImageWriter())
    ean13.write(buffer)
    buffer.seek(0)
    raw_bytes = buffer.getvalue()

    return BufferedInputFile(
        file=raw_bytes,
        filename=f"{sku_13}.png",
    )
    return buffer