import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import asyncio
from orders_manager import get_total_revenue, get_all_orders, add_order

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Все заказы")],
        [KeyboardButton(text="Добавить заказ")],
        [KeyboardButton(text="Показать Выручку")]
        
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

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("start", reply_markup=main_keyboard)

@dp.message(F.text == "Все заказы")
async def order_handler(message: types.Message):
    for order in get_all_orders():
        await message.answer(f"ID {order.id} | Клиент: {order.name} | Сумма заказа: {order.price} руб.")

@dp.message(F.text == "Показать Выручку")
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

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())