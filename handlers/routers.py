from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from handlers.generate_text import ai_generate
import handlers.keyboards as kb
from decouple import config
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='ai_bot.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


token = config("TELEGRAM_TOKEN")

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
    try:  
        price = int(message.text.split()[1])
        prices = [LabeledPrice(label="XTR", amount=price)]
        await bot.send_invoice(
            chat_id=message.chat.id,
            title="подписка Kitty GPT",  
            description=f"Купить подписку Kitty GPT\nЦена: {price}",  
            prices=prices,  
            provider_token="STARS",  
            payload="channel_support",  
            currency="XTR",  
            reply_markup=kb.buy_keyboard,  
        )
    except IndexError:
        await message.answer("Введите число после команды")
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
    await message.answer("Ваш запрос еще не обработан")

@router.message(F.text)
async def generating(message: Message, state: FSMContext):
    await state.set_state(ClientQuery.query)
    try:
        response, completion_tokens, prompt_tokens, total_tokens = await ai_generate(message.text, 'mistralai/mistral-saba')
        logger.info(f"completion_tokens: {completion_tokens}")
        logger.info(f"prompt_tokens: {prompt_tokens}")
        logger.info(f"total_tokens:{total_tokens}")
        await message.answer(response, parse_mode="Markdown")
    finally:
        await state.clear() 