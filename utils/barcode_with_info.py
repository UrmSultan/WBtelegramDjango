import io
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont
from aiogram.types import BufferedInputFile
import textwrap

# Размеры этикеток (в пикселях при 300 DPI)
LABEL_SIZES = {
    "small": (685, 472),  # 58×40 mm
    "medium": (1181, 591),  # 100×50 mm
    "large": (1181, 886),  # 100×75 mm
}

def generate_ean13_with_info(
        sku_13: str,
        title: str,
        brand: str,
        color: str,
        material: str,
        supplier_name: str,
        label_size="small"
) -> BufferedInputFile:
    width, height = LABEL_SIZES.get(label_size, LABEL_SIZES["small"])

    # Генерация штрих-кода
    buffer_barcode = io.BytesIO()
    ean13 = barcode.get_barcode_class("ean13")(sku_13, writer=ImageWriter())
    ean13.write(buffer_barcode)
    buffer_barcode.seek(0)
    barcode_img = Image.open(buffer_barcode).convert("RGBA")

    # Создаем белый холст
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)

    # Загружаем шрифт и корректируем размер
    try:
        font_size = int(height * 0.07)
        font = ImageFont.truetype("arial.ttf", font_size)
    except OSError:
        font = ImageFont.load_default()

    # Подготовка текста (убрали "Штрих-код" и "Пол")
    text_lines = [
        f"{supplier_name}",
        f"{title}",
        f"Цвет: {color}",
        f"Бренд: {brand}",
        f"Состав: {material}",
    ]

    # Перенос строк для длинных текстов
    wrapped_lines = []
    for line in text_lines:
        wrapped_lines.extend(textwrap.wrap(line, width=40))  # Регулируем ширину строки

    # Рисуем текст (ориентация слева, но с отступом)
    x_text = int(width * 0.05)  # Отступ слева
    y_text = int(height * 0.05)  # Отступ сверху

    line_spacing = 5  # Отступ между строками
    for line in wrapped_lines:
        draw.text((x_text, y_text), line, font=font, fill="black")
        y_text += font.getbbox(line)[3] + line_spacing  # Высота текста + отступ

    # Определяем размеры штрих-кода (сохранение пропорций)
    available_height = height - y_text - int(height * 0.05)  # Оставшееся место
    bc_w = int(width * 0.8)  # 80% ширины холста
    bc_h = min(int(bc_w * (barcode_img.height / barcode_img.width)), available_height)  # Авторазмер с ограничением

    # Проверяем, что штрих-код помещается
    if bc_h < 50:  # Минимальная высота для читаемости
        bc_h = 50
        bc_w = int(bc_h * (barcode_img.width / barcode_img.height))  # Коррекция ширины

    barcode_img = barcode_img.resize((bc_w, bc_h))

    # Размещаем штрих-код по центру
    barcode_top = y_text + 10
    canvas.paste(barcode_img, ((width - bc_w) // 2, barcode_top))

    # Сохраняем изображение
    output_buffer = io.BytesIO()
    canvas.save(output_buffer, format="PNG")
    output_buffer.seek(0)

    return BufferedInputFile(
        file=output_buffer.getvalue(),
        filename=f"{sku_13}.png"
    )
