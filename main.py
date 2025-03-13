from aiogram import Bot, Dispatcher
from handlers.routers import router
from handlers.db.db_core import init_db
from dotenv import load_dotenv
import os

load_dotenv('./.env')

async def main():
    await init_db()
    token = os.getenv("TELEGRAM_TOKEN")
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())