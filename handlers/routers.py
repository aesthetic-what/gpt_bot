from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from handlers.generate import ai_generate
import handlers.keyboards as kb

router = Router()

class ClientQuery(StatesGroup):
    query = State()

@router.message(CommandStart())
async def hello(message: Message):
    await message.answer("Привет, выбери гпт для запроса", reply_markup=kb.test_keyboard)
    
@router.callback_query(F.data == 'deepseek')
async def test_com(call: CallbackQuery):
    await call.message.answer("Введте запрос")

@router.message(ClientQuery.query)
async def flood(message: Message):
    await message.answer("Ваш запрос еще не обраотан")

@router.message(F.text)
async def generating(message: Message, state: FSMContext):
    await state.set_state(ClientQuery.query)
    response = await ai_generate(message.text, 'deepseek/deepseek-chat')
    await message.answer(response, parse_mode="Markdown")
    await state.clear()