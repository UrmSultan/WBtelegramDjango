from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import database
from keyboards.reply import auth_keyboard
from utils.parse_product import parse_characteristic
from api.products import get_wb_products

router = Router()

user_products = {}

# States for search query
class SearchState(StatesGroup):
    waiting_for_query = State()


@router.message(lambda message: message.text == "📦 Выбрать товар")
async def choose_product(message: Message):
    user_id = message.from_user.id
    wb_token = database.get_user_token(user_id)

    if not wb_token:
        await message.answer(
            "❌ Вы не авторизованы! Нажмите '🔑 Авторизоваться'",
            reply_markup=auth_keyboard()
        )
        return

    products = await get_wb_products(wb_token)

    if not products:
        await message.answer("❌ У вас нет товаров в Wildberries.")
        return

    user_products[user_id] = products

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔍 Поиск товара", callback_data="search")],
            [InlineKeyboardButton(text="🔍📋 Показать все", callback_data="show_all")]
        ]
    )

    await message.answer("📦 Ваши товары:", reply_markup=keyboard)

@router.callback_query(lambda call: call.data.startswith("product_"))
async def callback_product(call:CallbackQuery):
    user_id = call.from_user.id
    nm_id = call.data.removeprefix("product_")

    products = user_products.get(user_id,[])
    products = next((p for p in products if str(p["nmID"]) == nm_id), None)

    if not products:
        await call.message.answer("❌ Не могу найти этот товар в кэше. Попробуйте снова.")
        await call.answer()
        return

    sizes = products.get("sizes",[])
    if not sizes:
        await call.message.answer("❌ Для этого товара нет размеров.")
        await call.answer()
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=size.get("techSize", "NoSize"),
                    callback_data=f"size_{nm_id}_{size['chrtID']}_{size['skus'][0]}"
                )
            ]
            for size in sizes if size.get("skus")
        ]
    )
    await call.message.answer("Выберите размер:", reply_markup=keyboard)
    await call.answer()

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

@router.callback_query(lambda call: call.data == "show_all")
async def show_all_products(call: CallbackQuery):
    user_id = call.from_user.id
    products = user_products.get(user_id,[])

    if not products:
        await call.message.answer("❌ Список товаров пуст.")
        await call.answer()
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=f"{p.get('title', 'Без названия')} / {parse_characteristic(p, 'Цвет')}",
                callback_data=f"product_{p['nmID']}"
            )] for p in products[:10]
        ]
    )

    await call.message.answer("📋 Все доступные товары:", reply_markup=keyboard)
    await call.answer()