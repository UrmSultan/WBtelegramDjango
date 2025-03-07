import io
import barcode
from barcode.writer import ImageWriter
from PIL import ImageDraw, Image, ImageFont, UnidentifiedImageError
from aiogram.types import BufferedInputFile

def generate_ean13_with_info(
        sku_13: str,
        title: str,
        vendor_code: str,
        brand: str,
        color: str,
        gender: str,
        material: str,
        supplier_name: str
) -> BufferedInputFile:

    # Generate barcode
    buffer_barcode = io.BytesIO()
    ean13 = barcode.get_barcode_class("ean13")(sku_13, writer=ImageWriter())
    ean13.write(buffer_barcode)
    buffer_barcode.seek(0)

    # Open barcode in Pillow
    barcode_img = Image.open(buffer_barcode).convert("RGBA")
    bc_w, bc_h = barcode_img.size

    # Create new image (increased height)
    padding_top=250
    padding_bottom=50
    new_width = bc_w
    new_height = bc_h + padding_bottom + padding_top

    canvas = Image.new("RGB", (new_width, new_height), "white")
    draw = ImageDraw.Draw(canvas)

    # get font
    try:
        font = ImageFont.truetype("arial.ttf", size=24)
    except(OSError, UnidentifiedImageError):
        font = ImageFont.load_default()

    # Text preparation
    text_lines = [
        f"{supplier_name}",
        f"{title}",
        f"Артикул: {vendor_code}",
        f"Цвет: {color}",
        f"Пол: {gender}",
        f"Бренд: {brand}",
        f"Состав: {material}",
        f"Штрих-код {sku_13}",
    ]

    # Draw text in img
    x_text = 10
    y_text = 10
    dummy_draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    line_height = dummy_draw.textbbox((0, 0), "A", font=font)[3] + 5

    for line in text_lines:
        draw.text((x_text, y_text), line, font=font, fill="black")
        y_text+=line_height

    # Insert the barcode below the text
    barcode_top = y_text+10
    canvas.paste(barcode_img, (0, barcode_top), barcode_img)

    #
    output_buffer = io.BytesIO()
    canvas.save(output_buffer, format="PNG")
    output_buffer.seek(0)

    return BufferedInputFile(
        file=output_buffer.getvalue(),
        filename=f"{sku_13}.png"
    )