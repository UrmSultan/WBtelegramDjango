from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from utils.parse_product import parse_characteristic
from handlers.products import user_products

router = Router()

# States for search query
class SearchState(StatesGroup):
    waiting_for_query = State()


@router.callback_query(lambda call: call.data == "search")
async def start_search(call: CallbackQuery, state: FSMContext):
    await call.message.answer("🔍 Введите название, артикул или цвет товара:")
    await state.set_state(SearchState.waiting_for_query)
    await call.answer()

@router.message(SearchState.waiting_for_query)
async def process_search(message: Message, state: FSMContext):
    user_id = message.from_user.id
    query = message.text.lower()

    products = user_products.get(user_id,[])

    filtered_products = [
        p for p in products if
        query in p.get("title", "").lower() or
        query in p.get("vendorCode", "").lower() or
        query in parse_characteristic(p, "Цвет").lower()
    ]

    if not filtered_products:
        await message.answer("❌ Товары не найдены. Попробуйте другой запрос.")
        await state.clear()
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=f"{p.get('title', 'Без названия')} / {parse_characteristic(p, 'Цвет')}",
                callback_data=f"product_{p['nmID']}"
            )] for p in filtered_products[:10]
        ]
    )
    await message.answer("📋 Найденные товары:", reply_markup=keyboard)
    await state.clear()
