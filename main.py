# -*- coding: utf-8 -*-
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio
import logging

TOKEN = "7834299472:AAEUy5elgxbEvtmcbRqEi9U0j6MFRgCyiPo"
GROUP_ID = -1001260252066  # ← ваш chat_id группы

bot = Bot(token=TOKEN)
dp = Dispatcher()

class LeadForm(StatesGroup):
    room = State()
    goal = State()
    style = State()
    feeling = State()

@dp.message(F.text)
async def start(message: Message, state: FSMContext):
    kb = InlineKeyboardBuilder()
    kb.button(text="Начать подбор", callback_data="start")
    await message.answer(
        "🤍 Приветствуем вас в Фабрике Тканелье! Хотите подобрать идеальные шторы?",
        reply_markup=kb.as_markup()
    )

@dp.callback_query(F.data == "start")
async def ask_room(callback: CallbackQuery, state: FSMContext):
    kb = InlineKeyboardBuilder()
    for option in ["Гостиная", "Спальня", "Детская", "Кухня"]:
        kb.button(text=option, callback_data=f"room_{option}")
    await callback.message.answer("🕊️ Где вы планируете использовать шторы?", reply_markup=kb.as_markup())
    await state.set_state(LeadForm.room)

@dp.callback_query(F.data.startswith("room_"))
async def ask_goal(callback: CallbackQuery, state: FSMContext):
    await state.update_data(room=callback.data.split("_")[1])
    kb = InlineKeyboardBuilder()
    for option in ["Эстетика", "Затемнение", "Уют", "Приватность"]:
        kb.button(text=option, callback_data=f"goal_{option}")
    await callback.message.answer("🌿 Что для вас главное в шторах?", reply_markup=kb.as_markup())
    await state.set_state(LeadForm.goal)

@dp.callback_query(F.data.startswith("goal_"))
async def ask_style(callback: CallbackQuery, state: FSMContext):
    await state.update_data(goal=callback.data.split("_")[1])
    kb = InlineKeyboardBuilder()
    for option in ["Современный", "Классика", "Лофт", "Сканди"]:
        kb.button(text=option, callback_data=f"style_{option}")
    await callback.message.answer("🏡 В каком стиле у вас интерьер?", reply_markup=kb.as_markup())
    await state.set_state(LeadForm.style)

@dp.callback_query(F.data.startswith("style_"))
async def ask_feeling(callback: CallbackQuery, state: FSMContext):
    await state.update_data(style=callback.data.split("_")[1])
    kb = InlineKeyboardBuilder()
    for option in ["Покой", "Свежесть", "Тепло", "Лёгкость"]:
        kb.button(text=option, callback_data=f"feel_{option}")
    await callback.message.answer("💫 Какие эмоции хотите ощущать в комнате?", reply_markup=kb.as_markup())
    await state.set_state(LeadForm.feeling)

@dp.callback_query(F.data.startswith("feel_"))
async def submit(callback: CallbackQuery, state: FSMContext):
    await state.update_data(feeling=callback.data.split("_")[1])
    data = await state.get_data()
    text = (
        f"🎯 Новый лид от @{callback.from_user.username or 'без username'}:\n\n"
        f"🏠 Помещение: {data['room']}\n"
        f"🎯 Цель: {data['goal']}\n"
        f"🎨 Стиль: {data['style']}\n"
        f"💭 Эмоции: {data['feeling']}"
    )
    await bot.send_message(chat_id=GROUP_ID, text=text)
    await callback.message.answer("✅ Спасибо! Наш дизайнер скоро свяжется с вами.")
    await state.clear()

# Ответы на приветствия
@dp.message(F.text.lower().in_({"привет", "ау", "ты можешь общаться с клиентами?", "здравствуйте"}))
async def greeting_handler(message: Message):
    await message.answer("👋 Да, я ваш помощник от Фабрики Тканелье.\nГотов помочь с подбором штор!")

# Ответ на любое другое сообщение + отправка в группу
@dp.message()
async def fallback_handler(message: Message):
    await message.answer("Спасибо за сообщение! Я передам его менеджеру, а пока могу помочь с подбором штор 😊")
    text = (
        f"📩 Новый лид от @{message.from_user.username or 'без username'}\n\n"
        f"Сообщение: {message.text}"
    )
    try:
        await bot.send_message(chat_id=GROUP_ID, text=text)
    except Exception as e:
        await callback.message.answer(f"Ошибка при отправке в группу:\n<code>{e}</code>", parse_mode="HTML")

# Запуск
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
