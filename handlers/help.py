from aiogram import Router
from aiogram.types import Message, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMediaPhoto
import os

router = Router()

HELP_TEXT = {
    "ru":(
        "📌 *Как правильно напечатать этикетку:*\n\n"
        "1️⃣ Скачайте изображение с этикеткой.\n"
        "2️⃣ Откройте изображение и нажмите *Ctrl + P* (или кнопку 'Печать').\n"
        "3️⃣ В настройках печати установите:\n"
        "   - 📄 *Ориентация*: Книжная\n"
        "   - 🖨 *Количество копий*: нужное количество\n"
        "   - 📏 *Размер бумаги*: 58×40 мм\n"
        "   - 🖼 *Размер фотографии*: На всю страницу\n\n"
        "✅ После настройки нажмите 'Печать'."
    ),
    "kg": (
        "📌 *Этикетканы кантип туура басып чыгарса болот:*\n\n"
        "1️⃣ Этикетканын сүрөтүн жүктөп алыңыз.\n"
        "2️⃣ Сүрөттү ачып, *Ctrl + P* басыңыз (же 'Печать'(Басып чыгаруу) баскычын басыңыз).\n"
        "3️⃣ Басып чыгаруу орнотууларында төмөнкүлөрдү коюңуз:\n"
        "   - 📄 *Багыты(Ориентация)*: Тик (Книжная)\n"
        "   - 🖨 *Көчүрмөлөрдүн саны(Количество копий)*: Керектүү санда\n"
        "   - 📏 *Кагаздын өлчөмү(Размер бумаги)*: 58×40 мм\n"
        "   - 🖼 *Сүрөттүн өлчөмү(Размер фотографии)*: Толук бет\n\n"
        "✅ Орнотууларды бүтүргөндөн кийин 'Печать'(Басып чыгаруу) баскычын басыңыз."
    )
}

@router.message(lambda message: message.text == "ℹ️ Помощь")
async def help_command(message: Message):
    image_path="static/help_example.png"

    if not os.path.exists(image_path):
        await message.answer("❌ Ошибка: Изображение с инструкцией не найдено.")
        return

    help_image = FSInputFile(image_path)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇰🇬 Кыргызча", callback_data="help_kg")]
        ]
    )

    await message.answer_photo(
        photo=help_image,
        caption=HELP_TEXT["ru"],
        parse_mode="Markdown",
        reply_markup=keyboard
    )


@router.callback_query( lambda call: call.data == "help_kg")
async def help_kg(call: CallbackQuery):
    image_path="static/help_example.png"

    if not os.path.exists(image_path):
        await call.message.answer("❌ Ката: Нускама сүрөтү табылган жок.")
        return

    help_image = FSInputFile(image_path)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="help_ru")]
        ]
    )

    await  call.message.edit_media(
        media=InputMediaPhoto(media=help_image),
        reply_markup=keyboard
    )
    await call.message.edit_caption(
        caption=HELP_TEXT["kg"],
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    await call.answer()

@router.callback_query( lambda call: call.data == "help_ru")
async def show_russian_help(call: CallbackQuery):
    image_path="static/help_example.png"

    if not os.path.exists(image_path):
        await call.message.answer("❌ Ошибка: Изображение с инструкцией не найдено.")
        return

    help_image = FSInputFile(image_path)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇰🇬 Кыргызча", callback_data="help_kg")]
        ]
    )

    await call.message.edit_media(
        media=InputMediaPhoto(media=help_image),
        reply_markup=keyboard
    )

    await call.message.edit_caption(
        caption=HELP_TEXT["ru"],
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    await call.answer()