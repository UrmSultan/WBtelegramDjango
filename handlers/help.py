from aiogram import Router
from aiogram.types import Message, FSInputFile
import os

router = Router()

HELP_TEXT = (
"📌 *Как правильно напечатать этикетку:*\n\n"
    "1️⃣ Скачайте изображение с этикеткой.\n"
    "2️⃣ Откройте изображение и нажмите *Ctrl + P* (или кнопку 'Печать').\n"
    "3️⃣ В настройках печати установите:\n"
    "   - 📄 *Ориентация*: Книжная\n"
    "   - 🖨 *Количество копий*: нужное количество\n"
    "   - 📏 *Размер бумаги*: 58×40 мм\n"
    "   - 🖼 *Размер фотографии*: На всю страницу\n\n"
    "✅ После настройки нажмите 'Печать'."
)

@router.message(lambda message: message.text == "ℹ️ Помощь")
async def help_command(message: Message):
    image_path="static/help_example.png"

    if not os.path.exists(image_path):
        await message.answer("❌ Ошибка: Изображение с инструкцией не найдено.")
        return

    help_image = FSInputFile(image_path)
    await message.answer_photo(
        photo=help_image,
        caption=HELP_TEXT,
        parse_mode="Markdown",
    )
