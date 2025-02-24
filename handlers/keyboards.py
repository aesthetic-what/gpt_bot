from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

ai_models = ["deepseek/deepseek-chat", "cognitivecomputations/dolphin3.0-r1-mistral-24b:free"]
# print([name_gpt.split('/') for name_gpt in ai_models])

builder = InlineKeyboardBuilder()

for gpt_model in ai_models:
    button = InlineKeyboardButton(text=f'{gpt_model}', callback_data=f"{gpt_model}")
    builder.add(button)
    builder.adjust(2)
     
test_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='test', callback_data='deepseek')]])

buy_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='купить подписку', pay=True)]])

# Создаем клавиатуру с кнопками
keyboard = [
    [InlineKeyboardButton(text="Подтвердить оплату", callback_data="confirm")],
    [InlineKeyboardButton(text="Отменить", callback_data="cancel")]
]
reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)