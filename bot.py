import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
from orders_manager import get_total_revenue

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Welcome to Taxi Orders Manager!")
@dp.message(Command("revenue"))
async def revenue_handler(message: types.Message):
    await message.answer(f"Выручка составляет {str(get_total_revenue())} руб.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())