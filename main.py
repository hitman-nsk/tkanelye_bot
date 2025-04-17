import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram import F
import asyncio

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message(F.text | F.photo | F.video)
async def handle_message(message: Message):
    if message.text:
        await message.answer("📝 Принял текст, начинаем обработку...")
    elif message.photo:
        await message.answer("📷 Получено фото. Спасибо!")
    elif message.video:
        await message.answer("🎥 Видео получено. Обрабатываю...")
    else:
        await message.answer("Получено сообщение, спасибо!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())