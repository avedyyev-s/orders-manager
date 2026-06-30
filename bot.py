import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import asyncio
from orders_manager import get_total_revenue, get_all_orders, add_order, delete_order_by_id, search_orders
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Все заказы")],
        [KeyboardButton(text="Добавить заказ")],
        [KeyboardButton(text="Показать выручку")],
        [KeyboardButton(text="Удалить заказ")],
        [KeyboardButton(text="Поиск заказа")]
    ],
    resize_keyboard=True
)

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class OrderForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_price = State()
    waiting_for_id = State()
    waiting_for_search = State()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("start", reply_markup=main_keyboard)

@dp.message(F.text == "Все заказы")
async def order_handler(message: types.Message):
    for order in get_all_orders():
        await message.answer(f"ID {order.id} | Клиент: {order.name} | Сумма заказа: {order.price} руб.")

@dp.message(F.text == "Показать выручку")
async def revenue_handler(message: types.Message):
    await message.answer(f"Выручка составляет {str(get_total_revenue())} руб.")

@dp.message(F.text == "Добавить заказ")
async def process_start(message: types.Message, state: FSMContext):
    await state.set_state(OrderForm.waiting_for_name)
    await message.answer("Введите имя:")

@dp.message(OrderForm.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(OrderForm.waiting_for_price)
    await message.answer("Введите сумму:")

@dp.message(OrderForm.waiting_for_price)
async def process_price(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data.get("name")
    try:
        price = int(message.text)
    except(ValueError):
        await message.answer("Введите число!")
        return
    add_order(name, price)
    await state.clear()
    await message.answer("Заказ успешно добавлен!", reply_markup=main_keyboard)

@dp.message(F.text == "Удалить заказ")
async def process_delete_start(message: types.Message, state: FSMContext):
    await state.set_state(OrderForm.waiting_for_id)
    await message.answer("Введите ID удаляемого заказа:")

@dp.message(OrderForm.waiting_for_id)
async def process_delete(message: types.Message, state: FSMContext):
    try:
        order_id = int(message.text)
        if delete_order_by_id(order_id):
            await state.clear()
            await message.answer("Заказ успешно удален!", reply_markup=main_keyboard)
        else:
            await state.clear()
            await message.answer("Заказ с данным ID не найден!", reply_markup=main_keyboard)
    except(ValueError):
        await message.answer("Пожалуйста, введите ID цифрами!")
        return

@dp.message(F.text == "Поиск заказа")
async def process_search_start(message: types.Message, state: FSMContext):
    await state.set_state(OrderForm.waiting_for_search)
    await message.answer("Введите ID или имя заказа:")

@dp.message(OrderForm.waiting_for_search)
async def process_search(message: types.Message, state: FSMContext):
    user_answer = message.text
    orders = search_orders(user_answer)
    if len(orders) == 0:
        await message.answer("Ничего не найдено!", reply_markup=main_keyboard)
    else:
        for order in orders:
            await message.answer(f"ID {order.id} | Клиент: {order.name} | Сумма заказа: {order.price} руб.", reply_markup=main_keyboard)
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())