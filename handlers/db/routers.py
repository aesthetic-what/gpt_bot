from sqlalchemy import select, update, delete, insert
from handlers.db.models.users import Users, Content
from handlers.db.db_core import async_session

async def create_user(username: str, chat_id: int):
    async with async_session() as session:
        session.add(Content(content="1", user_id=chat_id))
        await session.commit()
    
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.tg_id == chat_id))
        if not user:
            session.add(Users(username=username, tg_id=chat_id))
            
        await session.commit()
        
async def update_content(chat_id: int, content: str):
    async with async_session() as session:
        await session.scalar(update(Content).values(content=content).where(Content.user_id == chat_id))
        await session.commit()