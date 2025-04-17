import os
import openai
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.types import Message
import asyncio

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Системные промпты для GPT-сотрудников
PROMPTS = {
    "content_creator": "Ты креативный сценарист и копирайтер. Придумай идею, заголовок и структуру текста на тему, которую прислал пользователь.",
    "marketer": "Ты маркетолог. Возьми текст и усили его: добавь УТП, триггеры, оффер и ориентируй на продажу. Не переписывай всё, а усили смысл.",
    "smm": "Ты эксперт по Telegram и Instagram. Адаптируй текст под формат Telegram, добавь хэштеги, предложения по визуалу. Сделай текст живым и вовлекающим."
}

async def query_gpt(role_prompt, user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": role_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    return response['choices'][0]['message']['content']

@dp.message(F.text)
async def handle_message(message: Message):
    user_input = message.text
    await message.answer("🧠 Обрабатываю ваш запрос через команду GPT-сотрудников...")

    try:
        # Шаг 1: Content Creator
        content_output = await query_gpt(PROMPTS["content_creator"], user_input)

        # Шаг 2: Маркетолог
        marketing_output = await query_gpt(PROMPTS["marketer"], content_output)

        # Шаг 3: SMM
        final_output = await query_gpt(PROMPTS["smm"], marketing_output)

        await message.answer("✅ Готово! Вот результат:\n\n" + final_output)

    except Exception as e:
        await message.answer(f"⚠️ Ошибка при генерации: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())