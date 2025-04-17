import os
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.types import Message
import asyncio

# Настройки
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1362399160350806167/MNFmKQ2MM3BVi84DS5MlBqTmPsORCPG6bgKXPvwMo7uFgBmghpZEBdb2QMikDtgDG5HJ"

bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Отправка промпта в Midjourney через Discord Webhook
def send_prompt_to_midjourney(prompt: str):
    content = f"/imagine {prompt}"
    response = requests.post(DISCORD_WEBHOOK_URL, json={"content": content})
    if response.status_code == 204:
        return "🎨 Промпт отправлен в Midjourney!"
    else:
        return f"⚠️ Ошибка Discord: {response.status_code} — {response.text}"

@dp.message(F.text)
async def handle_message(message: Message):
    user_input = message.text.strip()
    if not user_input:
        await message.answer("Пожалуйста, отправьте описание для изображения.")
        return

    await message.answer("📨 Получил описание. Отправляю в Midjourney...")
    feedback = send_prompt_to_midjourney(user_input)
    await message.answer(feedback)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())