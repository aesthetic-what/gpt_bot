from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types.star_transaction import StarTransaction
from handlers.generate import ai_generate
import handlers.keyboards as kb
from decouple import config

token = config("TELEGRAM_TOKEN")

# star = StarTransaction(id=str(uuid4()), amount=100, date=datetime.now())

# # Преобразуем данные в строку для отправки
# transaction_info = (
#     f"🔄 Транзакция: {star.id}\n"
#     f"💫 Количество звезд: {star.amount}\n"
#     f"📅 Дата: {star.date.strftime('%Y-%m-%d %H:%M:%S')}"
# )

router = Router()
bot = Bot(token)

class ClientQuery(StatesGroup):
    query = State()

@router.message(CommandStart())
async def hello(message: Message):
    await message.answer("Привет, выбери гпт для запроса", reply_markup=kb.test_keyboard)
    
    
# async def test_buy(message: Message):
#     await message.answer('Тестовая кнопка покупки', reply_markup=kb.buy_keyboard)
    
# @router.pre_checkout_query()
@router.message(Command('buy'))  
async def send_invoice_handler(message: Message):  
    prices = [LabeledPrice(label="XTR", amount=1)]  
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="подписку на услуги ГПТ",  
        description="Купить подписку ГПТ",  
        prices=prices,  
        provider_token="STARS",  
        payload="channel_support",  
        currency="XTR",  
        reply_markup=kb.buy_keyboard,  
    )
    
@router.pre_checkout_query()
async def on_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@router.message(F.successful_payment)
async def success_payment(message: Message):
    await message.answer('спасибо за покупку')

@router.callback_query(F.data == 'deepseek')
async def test_com(call: CallbackQuery):
    await call.message.answer("Введте запрос")

@router.message(ClientQuery.query)
async def flood(message: Message):
    await message.answer("Ваш запрос еще не обраотан")

@router.message(F.text)
async def generating(message: Message, state: FSMContext):
    await state.set_state(ClientQuery.query)
    response = await ai_generate(message.text, 'mistralai/codestral-2501')
    await message.answer(response, parse_mode="Markdown")
    await state.clear()