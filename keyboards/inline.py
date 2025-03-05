from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def product_keyboard(products):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=product.get("title", "Без названия"),
                callback_data=f"product_{product['nmID']}"
            )]
            for product in products[:10]
        ]
    )

def back_to_menu_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад в меню",callback_data="back_to_menu")]
        ]
    )