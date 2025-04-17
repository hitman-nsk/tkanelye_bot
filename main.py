import os
import openai
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.types import Message
import asyncio

# Настройки
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1362399160350806167/MNFmKQ2MM3BVi84DS5MlBqTmPsORCPG6bgKXPvwMo7uFgBmghpZEBdb2QMikDtgDG5HJ"

bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# GPT-инструкции
PROMPTS = {
    "content_creator": "Ты креативный сценарист. Придумай идею, заголовок и структуру текста на тему, которую прислал пользователь.",
    "marketer": "Ты маркетолог. Усиль текст: добавь УТП, триггеры, оффер и ориентацию на продажу.",
    "smm": "Ты SMM-специалист. Преобразуй текст под Telegram: добавь хэштеги, визуальные акценты, и опиши визуал для картинки."
}

# Запрос к GPT
async def query_gpt(role_prompt, user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": role_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    return response['choices'][0]['message']['content']

# Отправка промпта в Discord (Midjourney)
def send_prompt_to_midjourney(prompt: str):
    content = f"/imagine {prompt}"
    response = requests.post(DISCORD_WEBHOOK_URL, json={"content": content})
    if response.status_code == 204:
        return "🎨 Промпт отправлен в Midjourney!"
    else:
        return f"⚠️ Ошибка Discord: {response.status_code}"

@dp.message(F.text)
async def handle_message(message: Message):
    user_input = message.text
    await message.answer("🧠 Генерирую контент через команду GPT-сотрудников...")

    try:
        content_output = await query_gpt(PROMPTS["content_creator"], user_input)
        marketing_output = await query_gpt(PROMPTS["marketer"], content_output)
        smm_output = await query_gpt(PROMPTS["smm"], marketing_output)

        # Отправка промпта в Midjourney (берём описание из SMM)
        mj_feedback = send_prompt_to_midjourney(smm_output)

        await message.answer("✅ Готово!")

" + smm_output + "

" + mj_feedback)

    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
