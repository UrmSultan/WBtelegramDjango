import io
import barcode
from barcode.writer import ImageWriter

def generate_barcode(nm_id: str):
    buffer = io.BytesIO()
    code128 = barcode.get_barcode_class("code128")(nm_id, writer=ImageWriter())
    code128.write(buffer)
    buffer.seek(0)
    return buffer