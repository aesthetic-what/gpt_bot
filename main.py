from aiogram import Bot, Dispatcher
from handlers.routers import router
import os
from decouple import config

# load_dotenv('./.env')
# config = os.environ

async def main():
    token = config("TELEGRAM_TOKEN")
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())