from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def auth_keyboard():
    """Return keyboard for authorization."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔑 Авторизоваться")]],
        resize_keyboard=True
    )


def main_menu_keyboard():
    """Return keyboard for authenticated users."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Выбрать товар")],
            [KeyboardButton(text="ℹ️ Помощь")]],
        resize_keyboard=True
    )