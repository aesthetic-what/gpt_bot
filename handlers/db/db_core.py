from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

engine_url = 'sqlite+aiosqlite:///ai_bot.sqlite'

engine = create_async_engine(engine_url, echo=True)

class Base(DeclarativeBase): pass

async_session = async_sessionmaker(engine)

async def get_db():
    try:
        db = async_session()
    finally:
        db.close()
        
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
