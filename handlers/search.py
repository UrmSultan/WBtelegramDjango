from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


import database
from api import search_wb_products
from utils import parse_characteristic
from handlers.storage import user_products

router = Router()

# States for search query
class SearchState(StatesGroup):
    waiting_for_query = State()

@router.callback_query(lambda call: call.data == "search")
async def start_search_callback(call: CallbackQuery, state: FSMContext):
    await call.message.answer("🔍 Введите артикул или артикул продавца:")
    await state.set_state(SearchState.waiting_for_query)
    await call.answer()


@router.message(SearchState.waiting_for_query)
async def process_search_query(message: Message, state: FSMContext):
    user_id = message.from_user.id
    query = message.text.strip().lower()

    wb_token = database.get_user_token(user_id)
    if not wb_token:
        await message.answer("❌ Вы не авторизованы. Введите API-токен!")
        await state.clear()
        return

    products = await search_wb_products(wb_token, query, limit=10)
    if not products:
        retry_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔄 Повторить поиск", callback_data="search")],
            ]
        )
        await message.answer("❌ Товары не найдены. Попробуйте другой запрос.", reply_markup=retry_keyboard)
        await state.clear()
        return

    user_products[user_id] = products

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=f"{p.get('title', 'Без названия')} / {parse_characteristic(p, "Цвет")}",
                callback_data=f"product_{p['nmID']}"
            )] for p in products
        ]
    )
    await message.answer("📋 Найденные товары:", reply_markup=keyboard)
    await state.clear()
